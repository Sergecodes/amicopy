from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from ipware import get_client_ip
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import API_MESSAGE_TYPE, MAX_NUM_ONGOING_SESSIONS_UNAUTH_USERS
from .forms import SessionDevicesForm, SessionForm, SessionDevicesForm
from .models.models import Device, Transaction
from .serializers import SessionSerializer, TransactionSerializer
from .utils import get_session_or_404
from .validators import validate_user_create_session


@method_decorator(permission_classes([IsAuthenticated]), name='get')
@method_decorator(permission_classes([AllowAny]), name='post')
class SessionList(APIView):
    """List user's sessions or create new session"""

    def get(self, request, format=None):
        sessions = request.user.undeleted_sessions.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Required: 
            `title`(session title)
        Optional: 
            `code` (session creator code)
            `display_name`(device display name or nothing to use username), 
        """

        data, request_session, user = request.data, request.session, request.user
        # Verify if user is permitted.
        try:
            validate_user_create_session(user)
        except ValidationError as e:
            return Response({
                'message': e.message,
                'type': e.code
            }, status.HTTP_403_FORBIDDEN)

        session_form = SessionForm(data)
        session_device_form = SessionDevicesForm(user if user.is_authenticated else None, data)

        if not session_device_form.is_valid():
            return Response(session_device_form.errors.as_json(), status.HTTP_400_BAD_REQUEST)

        if session_form.is_valid():
            session_obj = session_form.save(commit=False)

            ip, is_routable = get_client_ip(request)
            device, is_new_device = Device.objects.get_or_create(
                browser_session_key=request_session._get_or_create_session_key(), 
                defaults={
                    'ip_address': ip,
                    'user': user if user.is_authenticated else None
                }
            )

            # Verify if device is permitted to create another session.
            if user.is_anonymous and not is_new_device and \
                device.num_ongoing_sessions == (count := MAX_NUM_ONGOING_SESSIONS_UNAUTH_USERS):
                return Response({
                    'message': _("You can be in at most %d active session") % count,
                    'type': API_MESSAGE_TYPE.UNAUTHENTICATED.value
                }, status.HTTP_403_FORBIDDEN)

            session_obj.creator_device = device
            # Pass creator_display_name to save() method, which will eventually be passed
            # to the post_save signal to be used by the SessionDevices to set the 
            # display_name attribute
            session_obj.save(
                creator_display_name=session_device_form.save(commit=False).display_name
            )
            return Response({
                'title': session_obj.title,
                'accepts_new_devices': session_obj.accepts_new_devices
            }, status.HTTP_201_CREATED)
        else:
            return Response(session_form.errors.as_json(), status.HTTP_400_BAD_REQUEST) 


@api_view(['GET', 'DELETE'])
@permission_classes([AllowAny])
def session_detail(request, uuid):
    """
    Retrieve or delete a session. 
    NOTE that anonymous users(devices) can only GET sessions.
    """
    found, result = get_session_or_404(uuid)
    if not found:
        return result

    session = result
    user = request.user

    if request.method == 'GET':
        serializer = SessionSerializer(session)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if user.is_anonymous:
            return Response({
                'type': API_MESSAGE_TYPE.UNAUTHENTICATED.value,
                'message': _('You need to be logged in to be able to delete a session')
            }, status.HTTP_401_UNAUTHORIZED)

        user.delete_session(session)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def transactions_list(request, session_uuid):
    found, result = get_session_or_404(session_uuid)
    user = request.user

    if found:
        session = result
        if user.is_authenticated:
            serializer = TransactionSerializer(user.get_transactions(session), many=True)
            return Response(serializer.data)
        else:
            device = Device.objects.filter(
                browser_session_key=request.session._get_or_create_session_key()
            ).first()

            if not device:
                return Response()
            else:
                serializer = TransactionSerializer(device.get_transactions(session), many=True)
                return Response(serializer.data)
    else:
        response = result
        return response


@api_view(['GET'])
@permission_classes([AllowAny])
def transaction_detail(request, session_uuid, transaction_uuid):
    """Retrieve a transaction from session_uuid and transaction_uuid"""
    found, result = get_session_or_404(session_uuid)

    if not found:
        response = result
        return response

    session = result
    transaction = get_object_or_404(Transaction, session_id=session.id, uuid=transaction_uuid)
    serializer = TransactionSerializer(transaction)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_session_exists(request, uuid):
    found, result = get_session_or_404(uuid)

    if found:
        session = result
        return Response({
            'title': session.title,
            'accepts_new_devices': session.accepts_new_devices
        })

    response = result
    return response


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_creator_code(request, code, uuid):
    found, result = get_session_or_404(uuid)

    if found:
        session = result
        creator_code = session.creator_code

        if not creator_code:
            # NOTE on client side, if session doesn't have creator code,
            # don't ask user to input it.
            return Response({
                'type': API_MESSAGE_TYPE.NO_CREATOR_CODE.value,
                'message': _('This session does not have a creator code')
            })

        if creator_code != code:
            return Response({
                'type': API_MESSAGE_TYPE.INVALID_CREATOR_CODE.value,
                'message': _('Incorrect code')
            }, status=status.HTTP_400_BAD_REQUEST)

    response = result
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_allow_new_devices(request, uuid):
    found, result = get_session_or_404(uuid)
    if not found:
        return result
        
    session = result
    
    # User should be owner of session
    if request.user != session.creator:
        return Response({
            'type': API_MESSAGE_TYPE.NOT_SESSION_OWNER.value,
            'message': _('You are not the owner of this session')
        }, status=status.HTTP_403_FORBIDDEN)

    if session.accepts_new_devices:
        session.block_new_devices()
        return Response({'type': API_MESSAGE_TYPE.NEW_DEVICES_BLOCKED.value})
    else:
        session.allow_new_devices()
        return Response({'type': API_MESSAGE_TYPE.NEW_DEVICES_ALLOWED.value})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_pin_session(request, uuid):
    found, result = get_session_or_404(uuid)
    if not found:
        return result
        
    session = result
    user = request.user

    if user.pinned_session:
        user.unpin_session()
        return Response({'type': API_MESSAGE_TYPE.UNPINNED_SESSION.value})
    else:
        try:
            user.pin_session(session)
        except ValidationError as e:
            return Response({
                'message': e.message,
                'type': e.code
            }, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'type': API_MESSAGE_TYPE.PINNED_SESSION.value})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_bookmark_transaction(request, uuid):
    transaction = get_object_or_404(Transaction, uuid=uuid)
    user = request.user

    if user.has_bookmarked_transaction(transaction):
        user.unbookmark_transaction(transaction, check=False)
        return Response({'type': API_MESSAGE_TYPE.REMOVED_BOOKMARK.value})
    else:
        try:
            user.bookmark_transaction(transaction, check=False)
        except ValidationError as e:
            return Response({
                'message': e.message,
                'type': e.code
            }, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'type': API_MESSAGE_TYPE.ADDED_BOOKMARK.value})


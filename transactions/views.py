from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from ipware import get_client_ip
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import API_MESSAGE_TYPE
from .forms import SessionForm
from .models.models import Device
from .serializers import SessionSerializer
from .utils import get_session_or_404


@method_decorator(permission_classes([IsAuthenticated]), name='get')
@method_decorator(permission_classes([IsAuthenticatedOrReadOnly]), name='post')
class SessionList(APIView):
    """List user's sessions or create new session"""

    def get(self, request, format=None):
        sessions = request.user.undeleted_sessions.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Required: title, display_name(device display name)
        Optional: code (creator code)
        """
        form = SessionForm(request.data)
        if form.is_valid():
            request_session, user = request.session, request.user
            session_obj = form.save(commit=False)

            ip, is_routable = get_client_ip(request)
            session_obj.creator_device = Device.objects.create(
                ip_address=ip, 
                display_name=request.data.get('display_name', user.username),
                browser_session_key=request_session._get_or_create_session_key(), 
                user=user if user.is_authenticated else None
            )

            session_obj.save()
            return Response({
                'title': session_obj.title,
                'accepts_new_devices': session_obj.accepts_new_devices
            }, status.HTTP_201_CREATED)
        else:
            return Response(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST) 


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
            }, status=status.HTTP_401_UNAUTHORIZED)

        user.delete_session(session)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
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
            'type': API_MESSAGE_TYPE.NOT_PERMITTED.value,
            'message': _('You are not the owner of this session')
        }, status=status.HTTP_403_FORBIDDEN)

    if session.accepts_new_devices:
        session.block_new_devices()
        return Response({'type': API_MESSAGE_TYPE.NEW_DEVICES_BLOCKED.value})
    else:
        session.allow_new_devices()
        return Response({'type': API_MESSAGE_TYPE.NEW_DEVICES_ALLOWED.value})


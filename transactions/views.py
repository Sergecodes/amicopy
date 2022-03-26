from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from ipware import get_client_ip
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import AJAX_MESSAGE_TYPE
from .forms import SessionForm
from .models.models import Device
from .serializers import SessionSerializer
from .utils import get_session_or_404


def test(request):
    return render(request, 'transactions/test.html')


class SessionList(APIView):
    """List user's sessions or create new session"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        sessions = request.user.undeleted_sessions.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        form = SessionForm(request.POST)
        if form.is_valid():
            request_session, user = request.session, request.user
            session_obj = form.save(commit=False)

            ip, is_routable = get_client_ip(request)
            session_obj.creator_device = Device.objects.create(
                ip_address=ip, 
                display_name=request.POST['display_name'],
                browser_session_key=request_session._get_or_create_session_key(), 
                user=user if user.is_authenticated else None
            )

            session_obj.save()
            return Response({
                'creator_code': session_obj.creator_code,
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
        if not user or user.is_anonumous:
            return Response({
                'msg_type': AJAX_MESSAGE_TYPE.NOT_PERMITTED
            }, status=status.HTTP_401_UNAUTHORIZED)

        user.delete_session(session)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def verify_session_exists(request, uuid):
    found, result = get_session_or_404(uuid)

    if found:
        session = result
        return Response({
            'creator_code': session.creator_code,
            'title': session.title,
            'accepts_new_devices': session.accepts_new_devices
        })

    response = result
    return response


@api_view(['GET'])
def verify_creator_code(request, uuid, code):
    found, result = get_session_or_404(uuid)

    if found:
        session = result
        creator_code = session.creator_code

        if not creator_code:
            return Response({'msg_type': AJAX_MESSAGE_TYPE.NO_CREATOR_CODE})

        if creator_code != code:
            return Response({
                'msg_type': AJAX_MESSAGE_TYPE.INVALID_CREATOR_CODE
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
            'msg_type': AJAX_MESSAGE_TYPE.NOT_PERMITTED
        }, status=status.HTTP_403_FORBIDDEN)

    if session.accepts_new_devices:
        session.block_new_devices()
    else:
        session.allow_new_devices()

    return Response()


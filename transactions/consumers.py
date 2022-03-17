import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer
from django.core.exceptions import ValidationError
from ipware import get_client_ip

from core.exceptions import WSClientError
from transactions.utils import get_device_or_error, get_session_or_error
from .models.models import Session, Transaction, Device


class SessionConsumer(AsyncJsonWebsocketConsumer):
    """
    This session consumer handles websocket connections for session clients.
    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """

    ##### WebSocket event handlers

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """

        # Create channel for current device, basically each device will be in a
        # singleton group
        await self.channel_layer.group_add(
            self.scope.session._get_or_create_session_key(),
            self.channel_name,
        )

        await self.accept()

        # Store which sessions the device has joined in this connection
        self.sessions = set()

    async def receive_json(self, content: dict):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a 'command' key we can switch on
        command = content.get('command')

        try:
            match command:
                case 'request_join':
                    # Send message to creator of session to add you to the session
                    await self.request_join_session(content['session_uuid'])
                case 'add': 
                    # Make them join the session
                    await self.add_to_session(content['session_uuid'], content['display_name'])
                case 'leave':
                    # Leave the session
                    await self.leave_session(content['session_uuid'], content['device_id'])
                case 'send':
                    await self.send_to_session(content['session_uuid'], content['message'])
                case __:
                    pass
        except WSClientError as e:
            # Catch any errors and send it back
            await self.send_json({ 'error': e.code })

    async def disconnect(self, code):
        """Called when the WebSocket closes for any reason."""

        # Leave all the sessions we are still in
        for session_uuid in list(self.sessions):
            try:
                await self.leave_session(session_uuid)
            except WSClientError:
                pass


    ##### Command helper methods called by receive_json

    async def request_join_session(self, session_uuid):
        """
        Called by receive_json when someone sends a request_join command.
        """
        await self.channel_layer.group_send(
            self.scope.session._get_or_create_session_key(),
            {
                'type': 'group.request_join',
                'session_uuid': session_uuid,
            }
        )

    async def add_to_session(self, session_uuid, display_name):
        """
        Called by receive_json when someone(session creator) sends an add command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        session = await get_session_or_error(session_uuid)

        # Add device to session
        request = self.scope
        user = request.user
        ip, is_routable = get_client_ip(request)
        browser_id = request.session._get_or_create_session_key()
        new_device = Device.objects.create(
            ip_address=ip, 
            display_name=display_name,
            browser_session_id=browser_id, 
            user=user if user.is_authenticated else None
        )

        try:
            session.add_device(new_device)
        except ValidationError as e:
            await self.send_json({
                "message": e.message,
                "msg_type": settings.fooo,
            })
            raise WSClientError(e.code.upper())

        # Add them to the group so they get session messages
        await self.channel_layer.group_add(
            session.group_name,
            self.channel_name,
        )

        # Store that we're in the session
        self.sessions.add(session_uuid)

        # Notify creator of session
        await self.channel_layer.group_send(
            browser_id,
            {
                'type': 'group.add',
                'session_uuid': session_uuid,
            }
        )

        # Instruct their client to finish opening the session (update ui, ...)
        await self.send_json({
            "add": session.uuid,
            "title": session.title,
        })

    async def leave_session(self, session_uuid, device_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        session = await get_session_or_error(session_uuid)
        device = await get_device_or_error(device_id)

        # Send a leave message 
        await self.channel_layer.group_send(
            self.scope.session._get_or_create_session_key(),
            {
                'type': "group.leave",
                'session_uuid': session_uuid,
            }
        )

        # Remove that we're in the session
        self.sessions.discard(session_uuid)

        # Remove them from the group so they no longer get session messages
        await self.channel_layer.group_discard(
            session.group_name,
            self.channel_name,
        )
        # Instruct their client to finish closing the session
        await self.send_json({
            "leave": session.uuid,
        })

    async def send_to_session(self, session_uuid, message):
        """
        Called by receive_json when someone sends a message to a session.
        """
        # Check they are in this session
        if session_uuid not in self.sessions:
            raise WSClientError("NOT_IN_SESSION")

        # Get the session and send to the group about it
        session = await get_session_or_error(session_uuid)
        await self.channel_layer.group_send(
            session.group_name,
            {
                'type': "group.message",
                'session_uuid': session_uuid,
                'message': message,
            }
        )

    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so group.add becomes group_add
    async def group_add(self, event):
        """
        Called when someone has joined our group.
        """
        # Send a message down to the client
        await self.send_json({
            "msg_type": settings.MSG_TYPE_ENTER,
            'session_uuid': event['session_uuid'],
        })

    async def group_leave(self, event):
        """
        Called when someone has left our group.
        """
        # Send a message down to the client
        await self.send_json({
            "msg_type": settings.MSG_TYPE_LEAVE,
            'session_uuid': event['session_uuid'],
        })

    async def group_message(self, event):
        """
        Called when someone has messaged our group.
        """
        # Send a message down to the client
        await self.send_json({
            "msg_type": settings.MSG_TYPE_MESSAGE,
            'session_uuid': event['session_uuid'],
            'message': event['message'],
        })

    async def group_request_join(self, event):
        """Called when someone asks group creator to join the group"""

        await self.send_json({
            "msg_type": settings.MSG_TYPE_REQUEST_JOIN,
            'session_uuid': event['session_uuid'],
        })


# See django-channels examples / multichat githup repo

class SessionConsumer(WebsocketConsumer):
    def connect(self):
        self.session_uuid = self.scope['url_route']['kwargs']['session_uuid']
        self.session_group_name = 'session_%s' % self.session_uuid
        self.session = Session.objects.get(uuid=self.session_uuid)

        request = self.scope
        user = request.user

        if user.is_anonymous:
            browser_key = request.session._get_or_create_session_key()
            ip, is_routable = get_client_ip(request)
            Device.objects.create(ip_address=ip)

        # Join session group
        async_to_sync(self.channel_layer.group_add)(
            self.session_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave session group
        async_to_sync(self.channel_layer.group_discard)(
            self.session_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        message = text_data_json['message']

        # Send message to session group
        async_to_sync(self.channel_layer.group_send)(
            self.session_group_name,
            {
                'type': command,
                'message': message
            }
        )

    # Join session group
    def join_session(self, event):
        request = self.scope
        user = request.user
        ip, is_routable = get_client_ip(request)
        browser_id = request.session._get_or_create_session_key()
        new_device = Device.objects.create(
            ip_address=ip, 
            display_name=event['display_name'],
            browser_session_id=browser_id, 
            user=user if user.is_authenticated else None
        )

        self.session.add_device(new_device)

        # Join session group
        async_to_sync(self.channel_layer.group_add)(
            self.session_group_name,
            self.channel_name
        )

    # Receive message from session group
    def group_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

        
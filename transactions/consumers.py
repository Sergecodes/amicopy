from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.exceptions import ValidationError
from ipware import get_client_ip

from core.exceptions import WSClientError
from .constants import WS_MESSAGE_TYPE
from .utils import get_device_or_error, get_session_or_error
from .models.models import Device


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
        await self.accept()

        # Store channel name of creator
        self.creator_channel_name = self.channel_name

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
                case 'end':
                    await self.end_session(content['session_uuid'], content['device_id'])
                case __:
                    pass
        except WSClientError as e:
            # Catch any errors and send it back
            await self.send_json({ 'error': e.code })

    async def disconnect(self, code):
        """Called when the WebSocket closes for any reason."""

        # Leave all the sessions we are still in
        for session_uuid in list(self.sessions):
            await self.leave_session(session_uuid)


    ##### Command helper methods called by receive_json

    async def request_join_session(self, session_uuid):
        """
        Called by receive_json when someone sends a request_join command.
        """
        await self.channel_layer.send(self.creator_channel_name, {
            'type': 'group.request_join',
            'session_uuid': session_uuid,
        })
        
    async def add_to_session(self, session_uuid, display_name):
        """
        Called by receive_json when someone(session creator) sends an add command.
        """

        @database_sync_to_async
        def get_or_create_device(data):
            return Device.objects.get_or_create(
                browser_session_key=data['browser_key'], 
                defaults={
                    'ip_address': data['ip'],
                    'display_name': data['display_name'],
                    'user': user if (user := data['user']).is_authenticated else None
                }
            )


        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        session = await get_session_or_error(session_uuid)

        # Add device to session
        request = self.scope
        ip, is_routable = get_client_ip(request)
        browser_key = request.session._get_or_create_session_key()

        device, is_new_device = await get_or_create_device({
            'browser_key': browser_key,
            'ip': ip,
            'user': request.user
        })

        try:
            await database_sync_to_async(session.add_device(device))()

            # Add them to the group so they get session messages
            await self.channel_layer.group_add(
                session.group_name,
                self.channel_name,
            )

            # Store that we're in the session
            self.sessions.add(session_uuid)

            # Notify creator of session
            await self.channel_layer.send(self.creator_channel_name, {
                'type': 'group.add',
                'session_uuid': session_uuid,
            })
        except ValidationError as e:
            await self.send_json({
                'message': e.message,
                'msg_type': WS_MESSAGE_TYPE.ERROR.value,
            })

    async def leave_session(self, session_uuid, device_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        session = await get_session_or_error(session_uuid)
        device = await get_device_or_error(device_id)

        # Send a leave message 
        await self.channel_layer.send(self.creator_channel_name, {
            'type': 'group.leave',
            'session_uuid': session_uuid,
        })

        await database_sync_to_async(device.leave_session(session))()

        # Remove that we're in the session
        self.sessions.discard(session_uuid)

        # Remove them from the group so they no longer get session messages
        await self.channel_layer.group_discard(
            session.group_name,
            self.channel_name,
        )

    async def send_to_session(self, session_uuid, message):
        """
        Called by receive_json when someone sends a message to a session.
        """
        # Check they are in this session
        if session_uuid not in self.sessions:
            raise WSClientError(WS_MESSAGE_TYPE.NOT_IN_SESSION.value)

        # Get the session and notify the group(session) of the message
        session = await get_session_or_error(session_uuid)

        await self.channel_layer.group_send(session.group_name, {
            'type': 'group.message',
            'session_uuid': session_uuid,
            'message': message,
        })

    async def end_session(self, session_uuid, device_id):
        """
        Called by receive_json when session is closed
        """
        session = await get_session_or_error(session_uuid)
        device = await get_device_or_error(device_id)

        try:
            await database_sync_to_async(device.end_session(session))()

            # Send end session message
            await self.channel_layer.group_send(session.group_name, {
                'type': 'group.end',
                'session_uuid': session_uuid,
            })

            # Remove that we're in the session
            self.sessions.discard(session_uuid)

            # Instruct client(creator) to finish closing the session
            # eg. remove session from ui, etc
            await self.send_json({
                'ended': session.uuid,
            })
        except ValidationError as e:
            await self.send_json({
                'message': e.message,
                'msg_type': WS_MESSAGE_TYPE.ERROR.value,
            })


    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so group.add becomes group_add
    async def group_add(self, event):
        """
        Called when someone has joined our group.
        """
        # Send a message down to the client
        await self.send_json({
            'msg_type': WS_MESSAGE_TYPE.ENTER.value,
            'session_uuid': event['session_uuid'],
        })

    async def group_leave(self, event):
        """
        Called when someone has left our group.
        """
        # Send a message down to the client
        await self.send_json({
            'msg_type': WS_MESSAGE_TYPE.LEAVE.value,
            'session_uuid': event['session_uuid'],
        })

    async def group_end(self, event):
        """
        Called when the group is ended
        """
        # Send a message down to the client
        await self.send_json({
            'msg_type': WS_MESSAGE_TYPE.SESSION_END.value,
            'session_uuid': event['session_uuid'],
        })

    async def group_message(self, event):
        """
        Called when someone has messaged our group.
        """
        # Send a message down to the client
        await self.send_json({
            'msg_type': WS_MESSAGE_TYPE.TRANSACTION.value,
            'session_uuid': event['session_uuid'],
            'message': event['message'],
        })

    async def group_request_join(self, event):
        """Called when someone asks group creator to join the group"""

        await self.send_json({
            'msg_type': WS_MESSAGE_TYPE.REQUEST_JOIN.value,
            'session_uuid': event['session_uuid'],
        })



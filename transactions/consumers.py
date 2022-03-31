from channels.exceptions import AcceptConnection, DenyConnection
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ipware import get_client_ip

from core.exceptions import WSClientError
from .constants import MAX_NUM_ONGOING_SESSIONS_UNAUTH_USERS, WS_MESSAGE_TYPE
from .models.models import Device, Transaction, TransactionToDevices
from .utils import (
    get_device_or_error, get_session_or_error, is_session_creator,
    get_or_create_device_via_browser,
)
from .validators import (
    validate_device_join_session,
    validate_user_join_session
)


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

        # TODO check if this the right ip address?
        request = self.scope
        print(request['client'])
        print(request['client'][0])

        ip, is_routable = get_client_ip(request)
        user, browser_key = request['user'], request['session']._get_or_create_session_key()

        device, is_new_device = await get_or_create_device_via_browser(
            browser_key,
            ip=ip,
            user=request['user'],
            display_name=request['url_route']['device_name']
        )

        try:
            session = await get_session_or_error(request['url_route']['session_uuid'])
        except WSClientError as e:
            raise DenyConnection(_('No such session exists'))

        # If user is anonymous, verify if limit for connections has reached
        if user.is_anonymous:
            try:
                validate_device_join_session(device)
            except ValidationError as e:
                # raise WSClientError(e.message, e.code)
                # print(f"You can be in at most {MAX_NUM_ONGOING_SESSIONS_UNAUTH_USERS} active sessions")
                # err_message = _("You can be in at most %d active session") % MAX_NUM_ONGOING_SESSIONS_UNAUTH_USERS
                raise DenyConnection(e.message)
        else:
            try:
                validate_user_join_session(user)
            except ValidationError as e:
                raise DenyConnection(e.message)
            
        # Accept connection and store connection creator
        await self.accept()
        cache.set(
            f'device_{device.uuid}_channel_name', 
            self.channel_name, 
            None
        )

        # Store channel name of creator
        # NOTE First device to join connection is creator.
        self.creator_channel_name = cache.get_or_set(
            f'session_{session.uuid}_creator_channel_name',
            self.channel_name,
            None
        )
        self.current_session = session
        self.device = device

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
                    await self.request_join_session(content['session_uuid'], content['display_name'])
                case 'add': 
                    # Make them join the session
                    await self.add_to_session(content['session_uuid'], content['display_name'])
                case 'leave':
                    # Leave the session
                    await self.leave_session(content['session_uuid'], content['device_uuid'])
                case 'message':
                    await self.message_session(
                        content['session_uuid'], 
                        content['device_uuid'],
                        content['sender_name'], 
                        content.get('title'),
                        content['message_shared'],
                        content.get('to_all', True),
                        content.get('target_ids', [])
                    )
                case 'end':
                    await self.end_session(content['session_uuid'], content['device_uuid'])
                case 'allow_devices':
                    await self.allow_new_devices(content['session_uuid'], content['device_uuid'])
                case 'block_devices':
                    await self.block_new_devices(content['session_uuid'], content['device_uuid'])
                case __:
                    pass
        except WSClientError as e:
            # Catch any error and send it back
            await self.send_json({
                'type': WS_MESSAGE_TYPE.ERROR.value, 
                'code': e.code, 
                'message': e.message
            })

    async def disconnect(self, close_code):
        """Called when the WebSocket closes for any reason."""
        @database_sync_to_async
        def get_device(session_key):
            return Device.objects.get(browser_session_key=session_key)

        try:
            device = await get_device(self.scope['session']._get_or_create_session_key())
        except Device.DoesNotExist:
            pass
        else:
            # Leave all the sessions we are still in
            for session_uuid in list(self.sessions):
                await self.leave_session(session_uuid, device)


    ##### Command helper methods called by receive_json

    async def request_join_session(self, session_uuid, display_name):
        """
        Called by receive_json when someone sends a request_join command.
        """
        await self.channel_layer.send(self.creator_channel_name, {
            'type': 'group.request_join',
            'session_uuid': session_uuid,
            'display_name': display_name
        })
        
    async def add_to_session(self, session_uuid, display_name):
        """
        Called by receive_json when someone(session creator) sends an add command.
        """

        @database_sync_to_async
        def device_in_session(device):
            return device in session.present_devices

        @database_sync_to_async
        def get_or_create_device(**data):
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
        browser_key = request['session']._get_or_create_session_key()

        device, is_new_device = await get_or_create_device(
            browser_key=browser_key,
            ip=ip,
            user=request['user'],
            display_name=display_name
        )

        if not await device_in_session(device):
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
                    'device': device
                })
            except ValidationError as e:
                # Raise this error so that it will be caught by receive_json method
                raise WSClientError(e.message, e.code)
        else:
            pass

    async def leave_session(self, session_uuid, device_or_id):
        """
        Called by receive_json when someone sends a leave command.
        """
        session = await get_session_or_error(session_uuid)

        if isinstance(device_or_id, int):
            device = await get_device_or_error(device_or_id)
        else:
            device = device_or_id

        if session_uuid in self.sessions:
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

    async def message_session(self, session_uuid, device_uuid, sender_name, title, message_shared, to_all: bool, target_ids: list):
        """
        Called by receive_json when someone sends a message to a session.
        """

        @database_sync_to_async
        def save_transaction_to_devices(bulk_list):
            TransactionToDevices.objects.bulk_create(bulk_list)

        @database_sync_to_async
        def set_transaction_devices(**kwargs):
            transaction = kwargs['transaction']
            target_devices_ids = kwargs['target_ids']

            if target_devices_ids:
                transaction.to_devices.set(target_devices_ids)
    

        # Check they are in this session
        if session_uuid not in self.sessions:
            raise WSClientError(
                _('You are not in this session'),
                WS_MESSAGE_TYPE.NOT_IN_SESSION.value
            )

        # Get the session and notify the group(session) of the message
        session = await get_session_or_error(session_uuid)
        device = await get_device_or_error(device_uuid)

        # Create transaction
        transaction = Transaction(
            title=title if title else '',
            text_content=message_shared,
            session=session,
            from_device=device
        )
        await database_sync_to_async(transaction.save)()

        if to_all:
            transaction_devices = []
            for device in session.present_devices:
                transaction_devices.append(
                    TransactionToDevices(transaction=transaction, device=device)
                )

                # Add them to the group so they get session messages
                await self.channel_layer.group_add(
                    transaction.group_name,
                    cache.get(f'device_{device.uuid}_channel_name'),
                )

            await save_transaction_to_devices(transaction_devices)
        else:
            await set_transaction_devices(transaction=transaction, target_ids=target_ids)

        await self.channel_layer.group_send(session.group_name, {
            'type': 'group.message',
            'sender_name': sender_name,
            'session_uuid': session_uuid,
            'message_shared': message_shared,
        })

    async def end_session(self, session_uuid, device_uuid):
        """
        Called by receive_json when session is closed
        """
        session = await get_session_or_error(session_uuid)
        device = await get_device_or_error(device_uuid)

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
                'type': WS_MESSAGE_TYPE.SESSION_ENDED.value,
                'session_uuid': session_uuid
            })
        except ValidationError as e:
            raise WSClientError(e.message, e.code)

    async def allow_new_devices(self, session_uuid, device_uuid):
        session = await get_session_or_error(session_uuid)
        device = await get_device_or_error(device_uuid)

        if await is_session_creator(device, session):
            await database_sync_to_async(session.allow_new_devices)()

            # Send message to creator
            await self.channel_layer.send(self.creator_channel_name, {
                'type': 'group.allow_new',
                'session_uuid': session_uuid,
            })

    async def block_new_devices(self, session_uuid, device_uuid):
        session = await get_session_or_error(session_uuid)
        device = await get_device_or_error(device_uuid)

        if await is_session_creator(device, session):
            await database_sync_to_async(session.block_new_devices)()

            # Send message to creator
            await self.channel_layer.send(self.creator_channel_name, {
                'type': 'group.block_new',
                'session_uuid': session_uuid,
            })


    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so group.add becomes group_add
    async def group_add(self, event: dict):
        """
        Called when someone has joined a group. 
        Sent to the group creator
        """
        # Send a message down to the client
        await self.send_json({
            'type': WS_MESSAGE_TYPE.ENTER.value,
            'message': _('%s has joined the session') % event['device'].display_name,
            'session_uuid': event['session_uuid'],
        })

    async def group_leave(self, event):
        """
        Called when someone has left our group. 
        Sent to the person who left
        """
        # Send a message down to the client
        await self.send_json({
            'type': WS_MESSAGE_TYPE.LEFT.value,
            'message': _('You left the session'),
            'session_uuid': event['session_uuid'],
        })

    async def group_end(self, event):
        """
        Called when the group is ended. Sent to all members
        """
        # Send a message down to the client
        await self.send_json({
            'type': WS_MESSAGE_TYPE.SESSION_ENDED.value,
            'message': _('Session has been ended'),
            'session_uuid': event['session_uuid'],
        })

    async def group_message(self, event):
        """
        Called when someone has messaged our group.
        Sent to all members
        """
        # Send a message down to the client
        await self.send_json({
            'type': WS_MESSAGE_TYPE.NEW_TRANSACTION.value,
            'sender_name': event['sender_name'],
            'session_uuid': event['session_uuid'],
            'message_shared': event['message_shared'],
        })

    async def group_request_join(self, event):
        """
        Called when someone asks group creator to join the group.
        Sent to group creator
        """

        await self.send_json({
            'type': WS_MESSAGE_TYPE.REQUEST_JOIN.value,
            'message': _('Let %s into the session') % event['display_name'],
            'session_uuid': event['session_uuid'],
        })

    async def group_allow_new(self, event):
        """
        Called when creator allows new devices. 
        Sent to group creator.
        """
        # Send a message down to the client
        await self.send_json({
            'type': WS_MESSAGE_TYPE.NEW_DEVICES_ALLOWED.value,
            'message': _('New devices can now join the session'),
            'session_uuid': event['session_uuid'],
        })

    async def group_block_new(self, event):
        """
        Called when creator blocks new devices. 
        Sent to group creator.
        """
        # Send a message down to the client
        await self.send_json({
            'type': WS_MESSAGE_TYPE.NEW_DEVICES_BLOCKED.value,
            'message': _('New devices have been blocked from joining the session'),
            'session_uuid': event['session_uuid'],
        })



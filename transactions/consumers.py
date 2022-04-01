from channels.exceptions import DenyConnection
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ipware import get_client_ip

from core.exceptions import WSClientError
from .constants import MAX_NUM_ONGOING_SESSIONS_UNAUTH_USERS, WS_MESSAGE_TYPE
from .models.models import Device, Session, Transaction, TransactionToDevices
from .utils import (
    get_transaction_or_error, get_session_or_error, 
    is_session_creator, get_or_create_device_via_browser,
)
from .validators import (
    validate_device_join_session, validate_auth_user,
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
            # If device is new, no need to peform these checks.
            # Since for now the only checks are to verify the number of ongoing sessions of
            # a device
            if not is_new_device:
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
        creator_cache_key = f'session_{session.uuid}_creator_channel_name'

        # If no creator key found in cache, then this is the first connection to the
        # session, so we can add session creator to group
        if not cache.get(creator_cache_key):
            await self.channel_layer.group_add(
                session.group_name,
                self.channel_name,
            )

        self.creator_channel_name = cache.get_or_set(
            creator_cache_key,
            self.channel_name,
            None
        )

        # Enable type highlighting 
        self.session: Session  = session
        self.device: Device = device

    async def receive_json(self, content: dict):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a 'command' key we can switch on
        command = content.get('command')
        user = self.scope['user']

        try:
            match command:
                case 'request_join':
                    # Send message to creator of session to add you to the session
                    await self.request_join_session()
                case 'add': 
                    # Make them join the session
                    await self.add_to_session()
                case 'leave':
                    # Leave the session
                    await self.leave_session()
                case 'message':
                    await self.message_session(
                        content.get('title'),
                        content['message_shared'],
                        content.get('to_all', True),
                        content.get('target_ids', [])
                    )
                case 'end':
                    await self.end_session()
                case 'allow_devices':
                    await self.allow_new_devices()
                case 'block_devices':
                    validate_auth_user(user)
                    await self.block_new_devices()
                case 'delete_for_self':
                    validate_auth_user(user)
                    await self.delete_message_for_self(content['message_uuid'])
                case 'delete_for_all':
                    validate_auth_user(user)
                    await self.delete_message_for_all(content['message_uuid'])
                case __:
                    pass
        except (WSClientError, ValidationError) as e:
            # Catch any error and send it back
            await self.send_json({
                'type': WS_MESSAGE_TYPE.ERROR.value, 
                'code': e.code, 
                'message': e.message
            })

    async def disconnect(self, close_code):
        """Called when the WebSocket closes for any reason."""

        await self.leave_session()


    ##### Command helper methods called by receive_json

    async def request_join_session(self):
        """
        Called by receive_json when someone sends a request_join command.
        """
        await self.channel_layer.send(self.creator_channel_name, {
            'type': 'group.request_join'
        })
        
    async def add_to_session(self):
        """
        Called by receive_json when someone(session creator) sends an add command.
        """
        @database_sync_to_async
        def device_in_session():
            return self.device in self.session.present_devices

        @database_sync_to_async
        def add_session_device():
            self.session.add_device(self.device)

        # Add device to session
        if not await device_in_session():
            try:
                await add_session_device()

                # Add them to the group so they get session messages
                await self.channel_layer.group_add(
                    self.session.group_name,
                    self.channel_name,
                )

                # Notify creator of session
                await self.channel_layer.send(self.creator_channel_name, {
                    'type': 'group.add'
                })
            except ValidationError as e:
                # Raise this error so that it will be caught by receive_json method
                raise WSClientError(e.message, e.code)

    async def leave_session(self):
        """
        Called by receive_json when someone sends a leave command.
        """
        @database_sync_to_async
        def leave_session():
            self.device.leave_session(self.session)

        await leave_session()

        # Remove deleted transaction uuids from cache 
        cache_key = f'device_{self.device.uuid}_deleted_transactions_uuids'
        cache.delete(cache_key)

        # Remove them from the group so they no longer get session messages
        await self.channel_layer.group_discard(
            self.session.group_name,
            self.channel_name,
        )

        # Send message to creator
        await self.channel_layer.send(self.creator_channel_name, {
            'type': 'group.leave',
        })

        # Notify creator
        await self.send_json({
            'type': WS_MESSAGE_TYPE.LEFT.value,
            'message': _('You left the session')
        })

    async def message_session(self, title, message_shared, to_all: bool, target_ids: list):
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

        # Create transaction
        transaction = Transaction(
            title=title if title else '',
            text_content=message_shared,
            session=self.session,
            from_device=device
        )
        await database_sync_to_async(transaction.save)()

        if to_all:
            transaction_devices = []
            for device in self.session.present_devices:
                transaction_devices.append(
                    TransactionToDevices(transaction=transaction, device=device)
                )

                # Add them to the transaction's group so they get session messages
                await self.channel_layer.group_add(
                    transaction.group_name,
                    cache.get(f'device_{device.uuid}_channel_name'),
                )
            await save_transaction_to_devices(transaction_devices)
        else:
            await set_transaction_devices(transaction=transaction, target_ids=target_ids)

        await self.channel_layer.group_send(self.session.group_name, {
            'type': 'group.message',
            'message_shared': message_shared,
        })

    async def end_session(self):
        """
        Called by receive_json when session is closed
        """
        @database_sync_to_async
        def close_session():
            self.device.end_session(self.session)

        try:
            await close_session()

            # Send end session message
            await self.channel_layer.group_send(self.session.group_name, {
                'type': 'group.end'
            })

            # Instruct client(creator) to finish closing the session
            # eg. remove session from ui, etc
            await self.send_json({
                'type': WS_MESSAGE_TYPE.SESSION_ENDED.value
            })
        except ValidationError as e:
            raise WSClientError(e.message, e.code)

    async def allow_new_devices(self):
        @database_sync_to_async
        def allow_devices():
            self.session.allow_new_devices()

        if await is_session_creator(self.device, self.session):
            await allow_devices()

            # Send message to creator
            await self.channel_layer.send(self.creator_channel_name, {
                'type': 'group.allow_new',
            })

    async def block_new_devices(self):
        @database_sync_to_async
        def block_devices():
            self.session.block_new_devices()

        if await is_session_creator(self.device, self.session):
            await block_devices()

            # Send message to creator
            await self.channel_layer.send(self.creator_channel_name, {
                'type': 'group.block_new',
            })

    async def delete_message_for_self(self, transaction_uuid):
        """Called when someone deletes a transaction for themself."""
        @database_sync_to_async
        def delete_message(transaction: Transaction):
            # Note there's a check in `receive_json` that verifies that user
            # is authenticated
            self.scope['user'].delete_transaction(transaction)
            
        transaction = await get_transaction_or_error(transaction_uuid)
        await delete_message(transaction)

        # Send message to user
        await self.send_json({
            'type': WS_MESSAGE_TYPE.TRANSACTION_DELETED.value,
            'message': _('Transaction deleted')
        })

    async def delete_message_for_all(self, transaction_uuid):
        """Called when transaction sender deletes a transaction."""
        @database_sync_to_async
        def delete_message(transaction: Transaction):
            self.scope['user'].delete_transaction(transaction, delete_for_all=True)
            
        transaction = await get_transaction_or_error(transaction_uuid)
        await delete_message(transaction)

        # Send end session message
        await self.channel_layer.group_send(self.session.group_name, {
            'type': 'group.message.delete'
        })

    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so group.add becomes group_add
    async def group_add(self, event):
        """
        Called when someone has joined a group. 
        Sent to the group creator.
        """
        # Send a message down to the client
        await self.send_json({
            'type': WS_MESSAGE_TYPE.ENTER.value,
            'message': _('%s has joined the session') % self.device.display_name
        })

    async def group_leave(self, event):
        """
        Called when someone has left our group. 
        Sent to the creator.
        """
        await self.send_json({
            'type': WS_MESSAGE_TYPE.LEFT.value,
            'message': _('%s left the session') % self.device.display_name
        })

    async def group_end(self, event):
        """
        Called when the group is ended. 
        Sent to all members
        """
        await self.send_json({
            'type': WS_MESSAGE_TYPE.SESSION_ENDED.value,
            'message': _('Session has been ended')
        })

    async def group_message(self, event):
        """
        Called when someone has messaged our group.
        Sent to all members
        """
        await self.send_json({
            'type': WS_MESSAGE_TYPE.NEW_TRANSACTION.value,
            'message_shared': event['message_shared'],
        })

    async def group_request_join(self, event):
        """
        Called when someone asks group creator to join the group.
        Sent to group creator
        """

        await self.send_json({
            'type': WS_MESSAGE_TYPE.REQUEST_JOIN.value,
            'message': _('Let %s into the session ?') % event['display_name']
        })

    async def group_allow_new(self, event):
        """
        Called when creator allows new devices. 
        Sent to group creator.
        """
        await self.send_json({
            'type': WS_MESSAGE_TYPE.NEW_DEVICES_ALLOWED.value,
            'message': _('New devices can now join the session')
        })

    async def group_block_new(self, event):
        """
        Called when creator blocks new devices. 
        Sent to group creator.
        """
        await self.send_json({
            'type': WS_MESSAGE_TYPE.NEW_DEVICES_BLOCKED.value,
            'message': _('New devices have been blocked from joining the session')
        })

    async def group_message_delete(self, event):
        """
        Called when transaction creator deletes transaction for all devices.
        Sent to group.
        """
        await self.send_json({
            'type': WS_MESSAGE_TYPE.TRANSACTION_DELETED.value,
            'message': _('Transaction deleted')
        })



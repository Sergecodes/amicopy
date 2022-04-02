from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from transactions.models.models import (
    Transaction, Device, Session,
    SessionDevices, 
)

User = get_user_model()


class DeviceTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', 
            email='user1@gmail.com',
            password='pip install'
        )
        self.device1 = Device.objects.create(user=self.user1)

    def test_device_without_name_gets_owner_username(self):
        """Device without a display_name should get the owner's name if owner exists"""
        self.assertEqual(self.device1.display_name, self.user1.username)

    def test_device_without_browser_id_and_user(self):
        """Device with browser session id but without creator and display name isn't created"""

        with self.assertRaises(ValidationError):
            Device.objects.create(display_name='tttt')
        

class SessionDevicesTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            username='user1', 
            email='user1@gmail.com',
            password='pip install'
        )
        creator_device1 = Device.objects.create(user=user1, display_name=user1.username)

        self.session1 = Session.objects.create(
            title='session 1',
            creator_device=creator_device1
        )
        self.new_device1 = Device.objects.create(user=user1, display_name='user1')
        self.new_device2 = Device.objects.create(user=user1, display_name='USER1')
        self.new_device3 = Device.objects.create(user=user1, display_name='nother name')

    def test_cannot_add_existing_device_name(self):
        """Cannot add a device with a name that exists to another device in the session"""

        # ValidationError should be raised since device with 
        with self.assertRaises(ValidationError):
            SessionDevices.objects.create(session=self.session1, device=self.new_device1)

        with self.assertRaises(ValidationError):
            SessionDevices.objects.create(session=self.session1, device=self.new_device2)

        sd_obj = SessionDevices(session=self.session1, device=self.new_device3)
        sd_obj.save()

        self.assertIsNotNone(sd_obj.pk)
        print(SessionDevices.objects.all())



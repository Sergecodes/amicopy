from django.contrib.auth import get_user_model
from django.test import TestCase
from transactions.models.models import Device

User = get_user_model()


class DeviceTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', 
            email='user1@gmail.com',
            password='pip install'
        )
        self.device1 = Device.objects.create(
            user=self.user1,
            display_name=self.user1.username,
        )

    def test_correct_ip_address(self):
        """Ip address is correct"""
        expected_ip = ''
        self.assertEqual(self.device1.ip_address, expected_ip)


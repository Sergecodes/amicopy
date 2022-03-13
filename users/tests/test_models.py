from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', 
            email='user1@gmail.com',
            password='pip install'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            email='user2@googlemail.com',
            password='pip install'
        )
        self.user3 = User.objects.create_user(
            username='user3', 
            email='USER3@GOOGLEMAIL.com',
            password='pip install'
        )

        # Note: should refresh from db to use the actual value stored in the db;
        # and not the attribute since the attribute still has googlemail in it.
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.user3.refresh_from_db()

    def test_email_field(self):
        """Email should be correctly parsed when creating user"""
        print(User.objects.all())

        self.assertEqual(self.user1.email, 'user1@gmail.com')
        self.assertEqual(self.user2.email, 'user2@gmail.com')
        self.assertEqual(self.user3.email, 'USER3@gmail.com')

    def test_email_in_query(self):
        """Email should be correctly parsed when used in a query"""
        self.assertEqual(User.objects.get(email='user2@gmail.com').username, 'user2')
        self.assertEqual(User.objects.get(email='user2@googlemail.com').username, 'user2')
        self.assertEqual(User.objects.get(email='user2@GOOGLEMAIL.com').username, 'user2')



from account.models import CustomUser, Address
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase


class CustomUserModelTestCase(TestCase):

    def test_create_user(self):

        user = CustomUser.objects.create(
            username='test_user',
            password='Test@1234',
            phone_number='09393214333',
            email='test@example.com',
            first_name='John',
            last_name='Doe',
            age=30,
            is_logged_in=False,
        )

        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.age, 30)
        self.assertFalse(user.is_logged_in)

    def test_invalid_phone_number(self):

        with self.assertRaises(ValidationError):
            CustomUser.objects.create(
                username='invalid_user',
                password='Test@1234',
                phone_number='0123456789',
                email='invalid@example.com',
            )

    def test_invalid_password(self):

        with self.assertRaises(ValidationError):
            CustomUser.objects.create(
                username='test_user',
                password='password',
                phone_number='09393214333',
                email='test@example.com',
            )

    def test_default_values(self):

        user = CustomUser.objects.create(
            username='default_user',
            password='Default@1234',
            phone_number='09393214333',
        )

        self.assertEqual(user.email, None)
        self.assertEqual(user.first_name, None)
        self.assertEqual(user.last_name, None)
        self.assertIsNone(user.age)
        self.assertFalse(user.is_logged_in)

    def test_superuser_default_values(self):

        user = CustomUser.objects.create_superuser(
            username='default_user',
            password='Default@1234',
            phone_number='09393214333',
        )

        self.assertEqual(user.email, '')
        self.assertEqual(user.first_name, None)
        self.assertEqual(user.last_name, None)
        self.assertIsNone(user.age)
        self.assertFalse(user.is_logged_in)


class AddressModelTestCase(TestCase):

    def setUp(self):

        self.user = CustomUser.objects.create(username='test_user', password='Test@1234', phone_number='09123456789')

    def test_create_address(self):

        address = Address.objects.create(
            user=self.user,
            country='USA',
            city='New York',
            address='123 Main St',
            zipcode='10001',
            is_active=True,
        )

        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(address.user, self.user)
        self.assertTrue(address.is_active)

    def test_activate_address(self):

        initial_address = Address.objects.create(
            user=self.user,
            country='USA',
            city='New York',
            address='123 Main St',
            zipcode='10001',
            is_active=True,
        )

        address2 = Address.objects.create(
            user=self.user,
            country='USA',
            city='Los Angeles',
            address='456 Oak St',
            zipcode='90001',
            is_active=False,
        )

        address2.activate()

        initial_address.refresh_from_db()
        address2.refresh_from_db()

        self.assertFalse(initial_address.is_active)

        self.assertTrue(address2.is_active)

    def test_unique_active_address(self):

        Address.objects.create(
            user=self.user,
            country='USA',
            city='New York',
            address='123 Main St',
            zipcode='10001',
            is_active=True
        )

        with self.assertRaises(IntegrityError):
            Address.objects.create(
                user=self.user,
                country='USA',
                city='Los Angeles',
                address='456 Oak St',
                zipcode='90001',
                is_active=True
            )

    def test_delete_address(self):

        address = Address.objects.create(
            user=self.user,
            country='USA',
            city='New York',
            address='123 Main St',
            zipcode='10001',
            is_active=True
        )

        address.delete()

        self.assertTrue(address.is_deleted)
        self.assertFalse(address.is_active)
        self.assertEqual(Address.objects.filter(id=address.id).count(), 0)

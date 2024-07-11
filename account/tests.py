from account.models import CustomUser, Address
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase


# noinspection PyUnusedLocal
class CustomUserModelTestCase(TestCase):

    def setUp(self):

        self.user_data = {
            'username': 'test_user',
            'password': 'Test@1234',
            'phone_number': '09115005055',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
        }

    # Create user tests
    def test_create_user_username(self):
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])

    def test_create_user_email(self):
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])

    def test_create_user_first_name(self):
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.first_name, self.user_data['first_name'])

    def test_create_user_last_name(self):
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.last_name, self.user_data['last_name'])

    def test_create_user_age(self):
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.age, self.user_data['age'])

    def test_create_user_is_logged_in(self):
        user = CustomUser.objects.create(**self.user_data)
        self.assertFalse(user.is_logged_in)

    # Read user tests
    def test_read_user_username(self):
        user_data = self.user_data.copy()
        user_data['phone_number'] = '09162806054'
        user_data['email'] = 'test2@example.com'
        user = CustomUser.objects.create(**user_data)
        fetched_user = CustomUser.objects.get(username=user_data['username'])
        self.assertEqual(fetched_user.username, user_data['username'])

    def test_read_user_email(self):
        user_data = self.user_data.copy()
        user_data['phone_number'] = '09162806054'
        user_data['email'] = 'test2@example.com'
        user = CustomUser.objects.create(**user_data)
        fetched_user = CustomUser.objects.get(username=user_data['username'])
        self.assertEqual(fetched_user.email, user_data['email'])

    def test_read_user_first_name(self):
        user_data = self.user_data.copy()
        user_data['phone_number'] = '09162806054'
        user_data['email'] = 'test2@example.com'
        user = CustomUser.objects.create(**user_data)
        fetched_user = CustomUser.objects.get(username=user_data['username'])
        self.assertEqual(fetched_user.first_name, user_data['first_name'])

    def test_read_user_last_name(self):
        user_data = self.user_data.copy()
        user_data['phone_number'] = '09162806054'
        user_data['email'] = 'test2@example.com'
        user = CustomUser.objects.create(**user_data)
        fetched_user = CustomUser.objects.get(username=user_data['username'])
        self.assertEqual(fetched_user.last_name, user_data['last_name'])

    def test_read_user_age(self):
        user_data = self.user_data.copy()
        user_data['phone_number'] = '09162806054'
        user_data['email'] = 'test2@example.com'
        user = CustomUser.objects.create(**user_data)
        fetched_user = CustomUser.objects.get(username=user_data['username'])
        self.assertEqual(fetched_user.age, user_data['age'])

    def test_read_user_is_logged_in(self):
        user_data = self.user_data.copy()
        user_data['phone_number'] = '09162806054'
        user_data['email'] = 'test2@example.com'
        user = CustomUser.objects.create(**user_data)
        fetched_user = CustomUser.objects.get(username=user_data['username'])
        self.assertFalse(fetched_user.is_logged_in)

    # Update user tests
    def test_update_user_first_name(self):
        user_data = self.user_data.copy()
        user_data['phone_number'] = '09167258466'
        user_data['email'] = 'test3@example.com'
        user = CustomUser.objects.create(**user_data)
        new_first_name = 'Jane'
        user.first_name = new_first_name
        user.save()
        updated_user = CustomUser.objects.get(username=user_data['username'])
        self.assertEqual(updated_user.first_name, new_first_name)

    # Delete user tests
    # noinspection PyTypeChecker
    def test_delete_user(self):
        user_data = self.user_data.copy()
        user_data['phone_number'] = '09304567820'
        user_data['email'] = 'test4@example.com'
        user = CustomUser.objects.create(**user_data)
        user_id = user.id
        user.delete()
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(id=user_id)

    # Validation tests
    def test_invalid_phone_number(self):
        invalid_user_data = self.user_data.copy()
        invalid_user_data['phone_number'] = '0123456789'
        invalid_user_data['email'] = 'invalid@example.com'
        with self.assertRaises(ValidationError):
            user = CustomUser(**invalid_user_data)
            user.full_clean()

    def test_invalid_password(self):
        invalid_user_data = self.user_data.copy()
        invalid_user_data['password'] = 'password'
        invalid_user_data['phone_number'] = '09162806054'
        invalid_user_data['email'] = 'invalid@example.com'
        with self.assertRaises(ValidationError):
            user = CustomUser(**invalid_user_data)
            user.full_clean()

    # Default values tests
    def test_default_values_email(self):
        minimal_user_data = {
            'username': 'default_user',
            'password': 'Default@1234',
            'phone_number': '09304567820',
            'email': 'default@example.com',
        }
        user = CustomUser.objects.create(**minimal_user_data)
        self.assertEqual(user.email, 'default@example.com')

    def test_default_values_first_name(self):
        minimal_user_data = {
            'username': 'default_user',
            'password': 'Default@1234',
            'phone_number': '09304567820',
            'email': 'default@example.com',
        }
        user = CustomUser.objects.create(**minimal_user_data)
        self.assertIsNone(user.first_name)

    def test_default_values_last_name(self):
        minimal_user_data = {
            'username': 'default_user',
            'password': 'Default@1234',
            'phone_number': '09304567820',
            'email': 'default@example.com',
        }
        user = CustomUser.objects.create(**minimal_user_data)
        self.assertIsNone(user.last_name)

    def test_default_values_age(self):
        minimal_user_data = {
            'username': 'default_user',
            'password': 'Default@1234',
            'phone_number': '09304567820',
            'email': 'default@example.com',
        }
        user = CustomUser.objects.create(**minimal_user_data)
        self.assertIsNone(user.age)

    def test_default_values_is_logged_in(self):
        minimal_user_data = {
            'username': 'default_user',
            'password': 'Default@1234',
            'phone_number': '09304567820',
            'email': 'default@example.com',
        }
        user = CustomUser.objects.create(**minimal_user_data)
        self.assertFalse(user.is_logged_in)

    # Superuser creation tests
    def test_create_superuser_username(self):
        superuser_data = {
            'username': 'super_user',
            'password': 'Super@1234',
            'phone_number': '09167258466',
            'email': 'super@example.com',
        }
        user = CustomUser.objects.create_superuser(**superuser_data)
        self.assertEqual(user.username, superuser_data['username'])

    def test_create_superuser_phone_number(self):
        superuser_data = {
            'username': 'super_user',
            'password': 'Super@1234',
            'phone_number': '09167258466',
            'email': 'super@example.com',
        }
        user = CustomUser.objects.create_superuser(**superuser_data)
        self.assertEqual(user.phone_number, superuser_data['phone_number'])

    def test_create_superuser_email(self):
        superuser_data = {
            'username': 'super_user',
            'password': 'Super@1234',
            'phone_number': '09167258466',
            'email': 'super@example.com',
        }
        user = CustomUser.objects.create_superuser(**superuser_data)
        self.assertEqual(user.email, superuser_data['email'])

    def test_create_superuser_is_superuser(self):
        superuser_data = {
            'username': 'super_user',
            'password': 'Super@1234',
            'phone_number': '09167258466',
            'email': 'super@example.com',
        }
        user = CustomUser.objects.create_superuser(**superuser_data)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_is_staff(self):
        superuser_data = {
            'username': 'super_user',
            'password': 'Super@1234',
            'phone_number': '09167258466',
            'email': 'super@example.com',
        }
        user = CustomUser.objects.create_superuser(**superuser_data)
        self.assertTrue(user.is_staff)


# noinspection PyUnusedLocal
class AddressModelTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='test_user',
            password='Test@1234',
            phone_number='09123456789',
            email='testemail1@gmail.com'
        )

    # Create Address Tests
    def test_create_address_count(self):
        address = Address.objects.create(
            user=self.user,
            country='USA',
            city='New York',
            address='123 Main St',
            zipcode='10001',
            is_active=True,
        )
        self.assertEqual(Address.objects.count(), 1)

    def test_create_address_user(self):
        address = Address.objects.create(
            user=self.user,
            country='USA',
            city='New York',
            address='123 Main St',
            zipcode='10001',
            is_active=True,
        )
        self.assertEqual(address.user, self.user)

    def test_create_address_is_active(self):
        address = Address.objects.create(
            user=self.user,
            country='USA',
            city='New York',
            address='123 Main St',
            zipcode='10001',
            is_active=True,
        )
        self.assertTrue(address.is_active)

    # Activate Address Tests
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

    # Unique Active Address Tests
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

    # Delete Address Tests
    def test_delete_address_is_deleted(self):
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

    def test_delete_address_is_inactive(self):
        address = Address.objects.create(
            user=self.user,
            country='USA',
            city='New York',
            address='123 Main St',
            zipcode='10001',
            is_active=True
        )

        address.delete()
        self.assertFalse(address.is_active)

    def test_delete_address_not_in_queryset(self):
        address = Address.objects.create(
            user=self.user,
            country='USA',
            city='New York',
            address='123 Main St',
            zipcode='10001',
            is_active=True
        )

        address_id = address.id
        address.delete()
        self.assertEqual(Address.objects.filter(id=address_id).count(), 0)

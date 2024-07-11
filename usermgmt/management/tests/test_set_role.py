from django.core.management import call_command
from django.core.management.utils import CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from io import StringIO


class SetRoleCommandTest(TestCase):

    def setUp(self):

        self.user = get_user_model().objects._create_user(
            phone_number='09123456789',
            email='testuser@example.com',
            password='Password123',
            username='testuser'
        )

        self.product_manager_group = Group.objects.create(name='Product Manager')
        self.supervisor_group = Group.objects.create(name='Supervisor')
        self.operator_group = Group.objects.create(name='Operator')

    def test_assign_product_manager_role(self):

        out = StringIO()

        call_command('set_role', '-u', 'testuser', '-P', stdout=out)

        self.user.refresh_from_db()
        self.assertTrue(self.user.groups.filter(name='Product Manager').exists())

    def test_assign_supervisor_role(self):

        out = StringIO()

        call_command('set_role', '-u', 'testuser', '-S', stdout=out)

        self.user.refresh_from_db()
        self.assertTrue(self.user.groups.filter(name='Supervisor').exists())

    def test_assign_operator_role(self):

        out = StringIO()

        call_command('set_role', '-u', 'testuser', '-O', stdout=out)

        self.user.refresh_from_db()
        self.assertTrue(self.user.groups.filter(name='Operator').exists())

    def test_assign_nonexistent_user(self):

        out = StringIO()

        with self.assertRaises(CommandError) as cm:
            call_command('set_role', '-u', 'nonexistentuser', '-P', stdout=out)
        self.assertEqual(str(cm.exception), 'User "nonexistentuser" does not exist')

    def test_no_role_flag_error(self):

        out = StringIO()

        with self.assertRaises(CommandError) as cm:
            call_command('set_role', '-u', 'testuser', stdout=out)
        self.assertEqual(str(cm.exception), 'No role specified. Use -P, -S, or -O to specify a role.')

    def test_user_already_has_role_message(self):

        self.user.groups.add(self.product_manager_group)
        self.user.save()

        out = StringIO()

        call_command('set_role', '-u', 'testuser', '-P', stdout=out)

        output = out.getvalue()
        self.assertIn('User "testuser" is already assigned to the role "Product Manager"', output)

    def test_no_action_performed_message(self):

        self.user.groups.add(self.product_manager_group)
        self.user.save()

        out = StringIO()

        call_command('set_role', '-u', 'testuser', '-P', stdout=out)

        output = out.getvalue()
        self.assertIn('No action had been performed', output)

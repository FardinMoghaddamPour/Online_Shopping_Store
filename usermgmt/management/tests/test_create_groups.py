from django.core.management import call_command
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from io import StringIO


class CreateGroupsCommandTest(TestCase):

    def setUp(self):

        out = StringIO()
        call_command('create_groups', stdout=out)

    def test_product_manager_group_created(self):
        self.assertTrue(Group.objects.filter(name='Product Manager').exists())

    def test_supervisor_group_created(self):
        self.assertTrue(Group.objects.filter(name='Supervisor').exists())

    def test_operator_group_created(self):
        self.assertTrue(Group.objects.filter(name='Operator').exists())

    def test_product_manager_permissions(self):
        product_manager_group = Group.objects.get(name='Product Manager')
        product_permissions = [
            'add_product', 'change_product', 'delete_product', 'view_product',
            'add_category', 'change_category', 'delete_category', 'view_category',
            'add_discount', 'change_discount', 'delete_discount', 'view_discount'
        ]
        for perm in product_permissions:
            with self.subTest(perm=perm):
                self.assertTrue(product_manager_group.permissions.filter(codename=perm).exists())

    def test_supervisor_permissions(self):
        supervisor_group = Group.objects.get(name='Supervisor')
        supervisor_permissions = Permission.objects.filter(codename__startswith='view_')
        for perm in supervisor_permissions:
            with self.subTest(perm=perm):
                self.assertTrue(supervisor_group.permissions.filter(codename=perm.codename).exists())

    def test_operator_permissions(self):
        operator_group = Group.objects.get(name='Operator')
        operator_permissions = [
            'add_customuser', 'change_customuser', 'delete_customuser', 'view_customuser',
            'add_order', 'change_order', 'delete_order', 'view_order',
            'add_address', 'change_address', 'delete_address', 'view_address'
        ]
        for perm in operator_permissions:
            with self.subTest(perm=perm):
                self.assertTrue(operator_group.permissions.filter(codename=perm).exists())

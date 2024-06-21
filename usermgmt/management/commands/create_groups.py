from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):

        product_manager_group, created = Group.objects.get_or_create(name='Product Manager')
        supervisor_group, created = Group.objects.get_or_create(name='Supervisor')
        operator_group, created = Group.objects.get_or_create(name='Operator')

        product_manager_permissions = Permission.objects.filter(
            content_type__model__in=[
                'product',
                'category',
                'discount'
            ],
            codename__in=[
                'add_product',
                'change_product',
                'delete_product',
                'view_product',
                'add_category',
                'change_category',
                'delete_category',
                'view_category',
                'add_discount',
                'change_discount',
                'delete_discount',
                'view_discount'
            ]
        )
        product_manager_group.permissions.set(product_manager_permissions)

        supervisor_permissions = Permission.objects.filter(codename__startswith='view')
        supervisor_group.permissions.set(supervisor_permissions)

        operator_permissions = Permission.objects.filter(
            content_type__model__in=[
                'customuser',
                'order',
                'address'
            ],
            codename__in=[
                'add_customuser',
                'change_customuser',
                'delete_customuser',
                'view_customuser',
                'add_order',
                'change_order',
                'delete_order',
                'view_order',
                'add_address',
                'change_address',
                'delete_address',
                'view_address'
            ]
        )
        operator_group.permissions.set(operator_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))

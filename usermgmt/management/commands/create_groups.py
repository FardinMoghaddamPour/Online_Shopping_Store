from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):

        created_any = False

        created_any |= self.create_group_with_permissions(
            'Product Manager',
            [
                'product',
                'category',
                'discount'
            ],
            [
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

        created_any |= self.create_group_with_permissions(
            'Supervisor',
            [],
            ['view_']
        )

        created_any |= self.create_group_with_permissions(
            'Operator',
            [
                'customuser',
                'order',
                'address'
            ],
            [
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

        if created_any:
            self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))
        else:
            self.stdout.write(self.style.WARNING('No action had been performed'))

    def create_group_with_permissions(self, group_name, models, codenames):

        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created group {group_name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Group {group_name} already exists'))

        if models:
            permissions = Permission.objects.filter(
                content_type__model__in=models,
                codename__in=codenames
            )
        else:
            permissions = Permission.objects.filter(codename__startswith=codenames[0])

        group.permissions.set(permissions)

        return created

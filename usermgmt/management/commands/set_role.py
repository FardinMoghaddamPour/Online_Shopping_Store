from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class Command(BaseCommand):

    help = 'Assign a role to a user'

    def add_arguments(self, parser):

        parser.add_argument('-u', '--username', type=str, required=True, help='The username of the user')
        parser.add_argument('-P', '--productManager', action='store_true', help='Assign Product Manager role')
        parser.add_argument('-S', '--supervisor', action='store_true', help='Assign Supervisor role')
        parser.add_argument('-O', '--operator', action='store_true', help='Assign Operator role')

    def handle(self, *args, **kwargs):

        username = kwargs['username']

        roles = {
            'productManager': 'Product Manager',
            'supervisor': 'Supervisor',
            'operator': 'Operator'
        }

        custom_user = get_user_model()

        try:
            user = custom_user.objects.get(username=username)
        except custom_user.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

        assigned_role = None

        for flag, role_name in roles.items():
            if kwargs[flag]:
                assigned_role = role_name
                break

        if not assigned_role:
            raise CommandError('No role specified. Use -P, -S, or -O to specify a role.')

        try:
            group = Group.objects.get(name=assigned_role)
        except Group.DoesNotExist:
            raise CommandError(f'Role "{assigned_role}" does not exist')

        if group in user.groups.all():

            self.stdout.write(
                self.style.WARNING(f'User "{username}" is already assigned to the role "{assigned_role}"')
            )
            self.stdout.write(
                self.style.WARNING('No action had been performed')
            )

        else:

            user.groups.add(group)
            user.is_staff = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully assigned role "{assigned_role}" to user "{username}"')
            )

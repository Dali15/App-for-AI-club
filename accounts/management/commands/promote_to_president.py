from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Promote an existing user to superuser/staff and set role to "president"'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to promote')

    def handle(self, *args, **options):
        username = options['username']
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

        user.is_staff = True
        user.is_superuser = True
        # set role safely if model has attribute
        if hasattr(user, 'role'):
            user.role = 'president'
        user.save()

        self.stdout.write(self.style.SUCCESS(f'User "{username}" promoted to superuser and role=president'))

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import json


class Command(BaseCommand):
    help = 'List users (id, username, email, is_active, is_superuser, role) as JSON'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=100, help='Maximum users to list')

    def handle(self, *args, **options):
        limit = options['limit']
        User = get_user_model()
        qs = User.objects.all().values('id', 'username', 'email', 'is_active', 'is_superuser', 'role')[:limit]
        self.stdout.write(json.dumps(list(qs), default=str))

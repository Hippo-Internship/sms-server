from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from core.apps.authapp import models as local_models

User = get_user_model()

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        user = User.objects.filter(is_superuser=True)
        if not user.exists():
            User.objects.create_superuser('admin@example.com', 'adminpass', groups=Group.objects.get(id=1))
            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % "superuser"))
        else:
            self.stdout.write(self.style.SUCCESS('Superadmin exists'))
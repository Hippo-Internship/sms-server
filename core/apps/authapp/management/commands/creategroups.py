from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from core.apps.authapp import models as local_models

User = get_user_model()

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        user = Group.objects.filter()
        if not user.exists():
            Group.objects.create(role_id=1, name="SuperAdmin")
            Group.objects.create(role_id=2, name="Admin")
            Group.objects.create(role_id=3, name="Operator")
            Group.objects.create(role_id=4, name="Teacher")
            Group.objects.create(role_id=5, name="Student")
            Group.objects.create(role_id=6, name="Accountant")
            Group.objects.create(role_id=7, name="Staff")
            self.stdout.write(self.style.SUCCESS('Groups added!'))
        else:
            self.stdout.write(self.style.SUCCESS('Groups exists!'))
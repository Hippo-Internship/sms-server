from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from core.apps.utilityapp import models as utility_models
from core.apps.datasheetapp import models as datasheetapp_models

User = get_user_model()

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # Default Status
        status_count = utility_models.Status.objects.count()
        if status_count == 0:
            utility_models.Status.objects.create(branch=None, name="Active", color="#70EE9C", default=True)
            utility_models.Status.objects.create(branch=None, name="Dropped", color="#DF3B57", default=True)
            utility_models.Status.objects.create(branch=None, name="Barter", color="#EF8354", default=True)
        else:
            self.stdout.write(self.style.NOTICE('Status exists!'))
        # Default Payment Method
        payment_method_count = utility_models.PaymentMethod.objects.count()
        if payment_method_count == 0:
            utility_models.PaymentMethod.objects.create(branch=None, name="Cash", default=True)
            utility_models.PaymentMethod.objects.create(branch=None, name="Credit Card", default=True)
        else:
            self.stdout.write(self.style.NOTICE('Payment method exists!'))
        # Default Datasheet Status Method
        datasheet_status_count = datasheetapp_models.Status.objects.count()
        if datasheet_status_count == 0:
            datasheetapp_models.Status.objects.create(branch=None, name="Active", default=True)
            datasheetapp_models.Status.objects.create(branch=None, name="Archive", default=True)
        else:
            self.stdout.write(self.style.NOTICE('Datasheet Status exists!'))
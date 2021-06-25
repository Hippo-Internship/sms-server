# Django imports
from django.shortcuts import render
# Third party imports
from rest_framework import \
        viewsets, \
        decorators as rest_decorators
# Local imports
from core import \
        responses as core_responses
from . import services as local_services

# Create your views here.
class DashboardViewset(viewsets.GenericViewSet):

    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="payment")
    def list_payment_data(self, request):
        income_data = local_services.generate_total_income_data(request.user)
        return core_responses.request_success_with_data()
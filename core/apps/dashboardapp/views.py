# Django imports
from django.shortcuts import render
# Third party imports
from rest_framework import \
        viewsets, \
        decorators as rest_decorators
# Local imports
from core import \
        responses as core_responses, \
        utils as core_utils
from . import services as local_services

# Create your views here.
class DashboardViewset(viewsets.GenericViewSet):

    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="payment")
    def list_payment_data(self, request):
        request_user = request.user
        query_params = core_utils.normalize_data(
            {
                "branch": "int",
                "school": "int",
                "filter": "int"
            },
            dict(request.query_params)
        )
        filter_model = {
            "branch": "student__user__branch",
            "school": "student__user__branch__school",
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        income_data = local_services.generate_total_income_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        return core_responses.request_success_with_data(income_data)
        
    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="student")
    def list_student_data(self, request):
        request_user = request.user
        query_params = core_utils.normalize_data(
            {
                "branch": "int",
                "school": "int",
                "filter": "int"
            },
            dict(request.query_params)
        )
        filter_model = {
            "branch": "student__user__branch",
            "school": "student__user__branch__school",
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        student_data = local_services.generate_students_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        return core_responses.request_success()
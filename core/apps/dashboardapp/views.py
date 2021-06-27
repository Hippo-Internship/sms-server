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
from core.apps.utilityapp import serializers as utilityapp_serializer
from core.apps.schoolapp import serializers as schoolapp_serializer
from core.apps.classapp import serializers as classapp_serializer
from . import services as local_services


filter_model = {
    "branch": "student__user__branch",
    "school": "student__user__branch__school",
}

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
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        income_data = local_services.generate_total_income_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        return core_responses.request_success_with_data(income_data)

    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="payment/branch")
    def list_payments_by_branch(self, request):
        request_user = request.user
        query_params = core_utils.normalize_data(
            {
                "school": "int",
                "filter": "int"
            },
            dict(request.query_params)
        )
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        branch_income_data = local_services.generate_payment_by_branch_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        p_branch_income_data = self.paginate_queryset(branch_income_data)
        branch_income_data = schoolapp_serializer.BranchWithAnnotationSerializer(p_branch_income_data, many=True)
        return self.get_paginated_response(branch_income_data.data)
        
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
            "branch": "branch",
            "school": "branch__school",
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        student_data = local_services.generate_students_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        return core_responses.request_success_with_data(student_data)

    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="payment/type")
    def list_payment_by_type(self, request):
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
            "branch": "branch",
            "school": "branch__school",
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        payment_by_type_data = local_services.generate_payment_by_type_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        p_payment_by_type_data = self.paginate_queryset(payment_by_type_data)
        payment_by_type_data = utilityapp_serializer.PaymentMethodWithAnnotation(p_payment_by_type_data, many=True)
        return self.get_paginated_response(payment_by_type_data.data)

    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="student/status")
    def list_student_by_status(self, request):
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
            "branch": "branch",
            "school": "branch__school",
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        student_by_status = local_services.generate_student_by_status_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        p_student_by_status = self.paginate_queryset(student_by_status)
        student_by_status = utilityapp_serializer.StatusWithAnnotation(p_student_by_status, many=True)
        return self.get_paginated_response(student_by_status.data)

    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="payment/lesson")
    def list_payment_by_lesson(self, request):
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
            "branch": "branch",
            "school": "branch__school",
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        student_data = local_services.generate_payment_by_lesson_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        p_student_data = self.paginate_queryset(student_data)
        student_data = classapp_serializer.LessonWithAnnotationSerializer(p_student_data, many=True)
        return self.get_paginated_response(student_data.data)
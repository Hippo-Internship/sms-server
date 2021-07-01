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
from core.apps.authapp import serializers as authapp_serializer
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
        _filter_model = {
            "branch": "branch",
            "school": "branch__school",
        }
        _filter_queries = core_utils.build_filter_query(_filter_model, query_params, user=request_user)
        income_data = local_services.generate_total_income_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1), add_filter_queries=_filter_queries)
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
        branch_income_data = schoolapp_serializer.BranchWithAnnotationSerializer(branch_income_data, many=True, context={ "request": request })
        return core_responses.request_success_with_data(branch_income_data.data)
        
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

    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="student/registered")
    def list_registered_student_data(self, request):
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
            "branch": "user__branch",
            "school": "user__branch__school",
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        student_data = local_services.generate_registered_students_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
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
        student_data = classapp_serializer.LessonWithAnnotationSerializer(student_data, many=True)
        return core_responses.request_success_with_data(student_data.data)

    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="datasheet")
    def list_datasheet_data(self, request):
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
        datasheet_data = local_services.generate_datasheet_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        return core_responses.request_success_with_data(datasheet_data) 

    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="datasheet")
    def list_datasheet_data(self, request):
        request_user = request.user
        query_params = core_utils.normalize_data(
            {
                "branch": "int",
                "school": "int",
                "filter": "int",
                "id": "int"
            },
            dict(request.query_params)
        )
        filter_model = {
            "branch": "branch",
            "school": "branch__school",
            "id": "operator__id"
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        datasheet_data = local_services.generate_datasheet_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        return core_responses.request_success_with_data(datasheet_data) 

    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="datasheet/operator")
    def list_datasheet_by_operator(self, request):
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
        student_data = local_services.generate_datasheet_by_operator_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        student_data = authapp_serializer.OperatorWithAnnotationSerializer(student_data, many=True, context={ "request": request })
        return core_responses.request_success_with_data(student_data.data)

    @rest_decorators.action(detail=False, methods=[ "GET" ], url_path="datasheet/type")
    def list_datasheet_by_register_type_data(self, request):
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
        datasheet_data = local_services.generate_datasheet_by_register_type_data(request_user, filter_queries=filter_queries, filter=query_params.get("filter", 1))
        return core_responses.request_success_with_data(datasheet_data) 
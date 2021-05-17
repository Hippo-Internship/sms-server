# Django built-in imports
from django.db.models import F
# Third Party imports
from rest_framework import viewsets
from rest_framework.settings import api_settings
# Local imports
from . import \
        models as local_models, \
        serializers as local_serializers, \
        services as local_services
from core import \
        decorators as core_decorators, \
        permissions as core_permissions, \
        responses as core_responses, \
        utils as core_utils


filter_model = {
    "class": "students___class",
    "lesson": "students___class__lesson",
    "payment": {
        "incomplete": {
            "name": "students__payment_paid",
            "value": F("students___class__lesson__price") - F("students__discount_amount")
        },
        "complete": {
            "name": "students__payment_paid",
            "value": F("students___class__lesson__price") - F("students__discount_amount")
        },
        "discount": "students__discount_amount"
    },
    "search": "phone"
}

class StudentViewSet(viewsets.GenericViewSet):

    queryset = local_models.User.objects.all()
    serializer_class = local_serializers.StudentCreateSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        core_permissions.StudentGetOrModifyPermission,
        core_permissions.BranchContentManagementPermission
    ]

    def list(self, request):
        query_params = core_utils.normalize_data(
            {
                "class": "int",
                "lesson": "int",
                "payment": "str",
                "search": "str",
                "status": "int"
            },
            dict(request.query_params)
        )
        filter_queries = core_utils.build_filter_query(filter_model, query_params)
        request_user = request.user
        if request_user.groups.role_id == local_models.User.SUPER_ADMIN:
            students = self.get_queryset().all(groups=local_models.User.STUDENT)
        elif request_user.groups.role_id == local_models.User.ADMIN:
            students = self.get_queryset().filter(
                branch__school=request_user.school.id, 
                groups__role_id=local_models.User.STUDENT, 
                **filter_queries
            )
        else:
            students = self.get_queryset().filter(
                branch=request_user.branch, 
                groups__role_id=local_models.User.STUDENT, 
                **filter_queries
            )
        p_students = self.paginate_queryset(students)
        students = self.get_serializer_class()(p_students, many=True)
        return self.get_paginated_response(students.data)

    @core_decorators.object_exists(model=local_models.User, detail="Student")
    def retrieve(self, request, student=None):
        student = self.get_serializer_class()(student, many=False)
        return core_responses.request_success_with_data(student.data)

    

    def get_serializer_class(self):
        if self.action == "list":
            return local_serializers.UserStudentsDetailSerializer
        elif self.action == "retrieve":
            return local_serializers.StudentFullDetailSerializer
        else:
            return super(StudentViewSet, self).get_serializer_class()
    

class DiscountViewSet(viewsets.ModelViewSet):

    queryset = local_models.Discount.objects.all()
    serializer_class = local_serializers.DiscountDetailSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.DiscountGetOrModifyPermission,
        core_permissions.BranchContentManagementPermission,
    ]

    def list(self, request):
        request_user = request.user
        discounts = local_services.list_discounts(request_user, self.get_queryset())
        p_discounts = self.paginate_queryset(discounts)
        discounts = self.get_serializer_class()(p_discounts, many=True)
        return self.get_paginated_response(discounts.data)

    @core_decorators.object_exists(model=local_models.Discount, detail="Discount")
    def retrieve(self, request, discount=None):
        data = super(DiscountViewSet, self).retrieve(request, discount.id).data
        return core_responses.request_success_with_data(data)

    def create(self, request):
        data = super(DiscountViewSet, self).create(request).data
        return core_responses.request_success_with_data(data)

    @core_decorators.object_exists(model=local_models.Discount, detail="Discount")
    def update(self, request, discount=None):
        data = super(DiscountViewSet, self).update(request, discount.id).data
        return core_responses.request_success_with_data(data)


class PaymentViewSet(viewsets.ModelViewSet):

    queryset = local_models.Payment.objects.all()
    serializer_class = local_serializers.PaymentSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.PaymentGetOrModifyPermission,
    ]

    def list(self, request):
        pass

    @core_decorators.object_exists(model=local_models.Student, detail="Student")
    def retrieve(self, request, student=None):
        payments = student.payments.all()
        p_payments = self.paginate_queryset(payments)
        payments = self.get_serializer_class()(p_payments, many=True)
        return self.get_paginated_response(payments.data)

    def create(self, request):
        data = super(PaymentViewSet, self).create(request).data
        return core_responses.request_success_with_data(data)

    @core_decorators.object_exists(model=local_models.Student, detail="Student")
    def update(self, request, student=None):
        data = super(PaymentViewSet, self).update(request, student.id).data
        return core_responses.request_success_with_data(data)
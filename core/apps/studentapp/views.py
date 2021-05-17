# Django built-in imports
from django.db.models import F
# Third Party imports
from rest_framework import \
        viewsets, \
        decorators as rest_decorators
from rest_framework.exceptions import PermissionDenied
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

    @rest_decorators.action(detail=True, methods=[ "GET" ], url_path="payment")
    @core_decorators.object_exists(model=local_models.Student, detail="Student")
    def list_payments(self, request, student=None):
        payments = student.payments.all()
        p_payments = self.paginate_queryset(payments)
        payments = self.get_serializer_class()(p_payments, many=True)
        return self.get_paginated_response(payments.data)

    @list_payments.mapping.post
    @core_decorators.object_exists(model=local_models.Student, detail="Student")
    def create_payment(self, request, student=None):
        payment_request_data = request.data
        request_user = request.user
        if request_user.groups.role_id == local_models.User.ADMIN:
            if not request_user.school.branches.filter(id=student.user.branch.id).exists():
                raise PermissionDenied()
        elif request_user.groups.role_id == local_models.User.OPERATOR:
            if request_user.branch.id != student.user.branch.id:
                raise PermissionDenied()
        payment_request_data["student"] = student.id
        payment = self.get_serializer_class()(data=payment_request_data) 
        payment.is_valid(raise_exception=True)
        payment.save()
        return core_responses.request_success_with_data(payment.data)


    @rest_decorators.action(detail=True, methods=[ "GET" ], url_path="note")
    @core_decorators.object_exists(model=local_models.Student, detail="Student")
    def list_notes(self, request, student=None):
        notes = student.notes.all()
        p_notes = self.paginate_queryset(notes)
        notes = self.get_serializer_class()(p_notes, many=True)
        return self.get_paginated_response(notes.data)

    @list_notes.mapping.post
    @core_decorators.object_exists(model=local_models.Student, detail="Student")
    def create_note(self, request, student=None):
        note_request_data = request.data
        request_user = request.user
        if request_user.groups.role_id == local_models.User.ADMIN:
            if not request_user.school.branches.filter(id=student.user.branch.id).exists():
                raise PermissionDenied()
        elif request_user.groups.role_id == local_models.User.OPERATOR:
            if request_user.branch.id != student.user.branch.id:
                raise PermissionDenied()
        note_request_data["student"] = student.id
        note = self.get_serializer_class()(data=note_request_data)
        note.is_valid(raise_exception=True)
        note.save()
        return core_responses.request_success_with_data(note.data)

    def get_serializer_class(self):
        if self.action == "list":
            return local_serializers.UserStudentsDetailSerializer
        elif self.action == "retrieve":
            return local_serializers.StudentFullDetailSerializer
        elif self.action == "list_payments" or self.action == "create_payment":
            return local_serializers.PaymentSerializer
        elif self.action == "list_notes" or self.action == "create_note":
            return local_serializers.NoteSerializer
        elif self.action == "update_note":
            return local_serializers.NoteUpdateSerializer
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


class PaymentViewSet(viewsets.GenericViewSet):

    queryset = local_models.Payment.objects.all()
    serializer_class = local_serializers.PaymentUpdateSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.PaymentGetOrModifyPermission,
    ]

    @core_decorators.object_exists(model=local_models.Payment, detail="Payment")
    def update(self, request, payment=None):
        payment_request_data = request.data
        request_user = request.user
        if request_user.groups.role_id == local_models.User.ADMIN:
            if not request_user.school.branches.filter(id=payment.student.user.branch.id).exists():
                raise PermissionDenied()
        elif request_user.groups.role_id == local_models.User.OPERATOR:
            if request_user.branch.id != payment.student.user.branch.id:
                raise PermissionDenied()
        payment = self.get_serializer_class()(payment, data=payment_request_data)
        payment.is_valid(raise_exception=True)
        payment.save()
        return core_responses.request_success_with_data(payment.data)

    @core_decorators.object_exists(model=local_models.Payment, detail="Payment")
    def destroy(self, request, payment=None):
        request_user = request.user
        if request_user.groups.role_id == local_models.User.ADMIN:
            if not request_user.school.branches.filter(id=payment.student.user.branch.id).exists():
                raise PermissionDenied()
        elif request_user.groups.role_id == local_models.User.OPERATOR:
            if request_user.branch.id != payment.student.user.branch.id:
                raise PermissionDenied()
        payment.delete()
        return core_responses.request_success()


class NoteViewSet(viewsets.GenericViewSet):

    queryset = local_models.Note
    serializer_class = local_serializers.NoteUpdateSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.NoteGetOrModifyPermission,
    ]

    @core_decorators.object_exists(model=local_models.Note, detail="Note")
    def update(self, request, note=None):
        note_request_data = request.data
        request_user = request.user
        if request_user.groups.role_id == local_models.User.ADMIN:
            if not request_user.school.branches.filter(id=note.student.user.branch.id).exists():
                raise PermissionDenied()
        elif request_user.groups.role_id == local_models.User.OPERATOR:
            if request_user.branch.id != note.student.user.branch.id:
                raise PermissionDenied()
        note = self.get_serializer_class()(note, data=note_request_data)
        note.is_valid(raise_exception=True)
        note.save()
        return core_responses.request_success_with_data(note.data)

    @core_decorators.object_exists(model=local_models.Note, detail="Note")
    def destroy(self, request, note=None):
        request_user = request.user
        if request_user.groups.role_id == local_models.User.ADMIN:
            if not request_user.school.branches.filter(id=note.student.user.branch.id).exists():
                raise PermissionDenied()
        elif request_user.groups.role_id == local_models.User.OPERATOR:
            if request_user.branch.id != note.student.user.branch.id:
                raise PermissionDenied()
        note.delete()
        return core_responses.request_success()
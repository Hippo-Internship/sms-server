# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError, NotFound
# Local imports
from core.apps.schoolapp import models as schoolapp_models


# User model
User = get_user_model()

def generate_basic_permission_switch(app_name, model_name):
    return {
        "list": app_name + ".view_" + model_name,
        "create": app_name + ".add_" + model_name,
        "update": app_name + ".change_" + model_name,
        "destroy": app_name + ".delete_" + model_name,
        "retrieve": app_name + ".view_" + model_name,
    }


class BranchContentManagementPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.groups.role_id == User.SUPER_ADMIN:
            return True
        if view.action == "create" or view.action == "update" or (hasattr(view, "additional_action") and view.action in view.additional_action):
            request_data = request.data
            branch_id = request_data.get("branch", -1)
            if branch_id == -1:
                raise NotFound({ "detail": "branch is not given!", "success": False })
            if user.groups.role_id == User.ADMIN:
                branch = schoolapp_models.Branch.objects.filter(id=branch_id)
                if not branch.exists():
                    raise NotFound({ "detail": "Branch does not exist!", "success": False })
                branch = branch[0]
                if branch.school.id is user.school.id:
                    return True
                else:
                    return False
            if branch_id != user.branch.id:
                return False
        elif view.action == "retrieve" or view.action == "destroy" or (hasattr(view, "detail_additional_action") and view.action in view.detail_additional_action):
            _object = view.get_queryset().filter(id=view.kwargs["pk"])
            if not _object.exists():
                raise NotFound({ "detail": "Object does not exist!", "success": False })
            _object = _object[0]
            if user.groups.role_id == User.ADMIN:
                if _object.branch.school.id != user.school.id:
                    return False
                else:
                    return True
            if _object.branch.id != user.branch.id:
                return False
        return True


class SchoolContentManagementPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.groups.role_id == User.SUPER_ADMIN:
            return True
        if view.action == "create" or view.action == "update":
            request_data = request.data
            try:
                school_id = int(request_data.get("school", -1))
            except:
                raise NotFound({ "detail": "school is not given!", "success": False })
            if school_id == None:
                raise NotFound({ "detail": "school is not given!", "success": False })
            if user.groups.role_id == User.ADMIN:
                if school_id != user.school.id:
                    return False
                else:
                    print("dqwdwq")
                    return True
            if school_id != user.school.id:
                return False
        elif view.action == "retrieve" or view.action == "destroy":
            _object = view.get_queryset().filter(id=view.kwargs["pk"])
            if not _object.exists():
                raise NotFound({ "detail": "Object does not exist!", "success": False })
            _object = _object[0]
            if user.groups.role_id == User.ADMIN:
                if _object.school.id != user.school.id:
                    return False
                else:
                    return True
            if _object.branch.school.id != user.school.id:
                return False
        return True


class StudentContentManagementPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.groups.role_id == User.SUPER_ADMIN:
            return True
        if view.action == "create" or (hasattr(view, "additional_action") and view.action in view.additional_action):
            request_data = request.data
            student_id = int(request_data.get("student", -1))
            if student_id == -1:
                raise NotFound({ "detail": "student is not given!", "success": False })
            student = view.get_queryset().filter(id=view.kwargs["pk"])
            if not student.exists():
                raise NotFound({ "detail": "Object does not exist!", "success": False })
            student = student[0]
            if user.groups.role_id == User.ADMIN:
                if not user.school.branches.filter(id=student.user.branch.id).exists():
                    return False
            elif user.groups.role_id == User.OPERATOR:
                if user.branch.id != student.user.branch.id:
                    return False
        if view.action == "retrieve" or view.action == "update" or view.action == "destroy" or (hasattr(view, "student_detail_additional_action") and view.action in view.student_detail_additional_action):
            _object = view.get_queryset().filter(id=view.kwargs["pk"])
            if not _object.exists():
                raise NotFound({ "detail": "Object does not exist!", "success": False })
            _object = _object[0]
            if not view.get_permission_query():
                _object = _object.student
            if user.groups.role_id == User.ADMIN:
                if not user.school.branches.filter(id=_object.user.branch.id).exists():
                    return False
            elif user.groups.role_id == User.OPERATOR:
                if user.branch.id != _object.user.branch.id:
                    return False
        return True


class UserGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        app_name = "authapp"
        model_name = "customuser"
        switch = generate_basic_permission_switch(app_name, model_name)
        switch["group"] = app_name + ".view_" + model_name
        return user.has_perm(switch.get(view.action, ""))


class SchoolGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("schoolapp", "school")
        switch["list_school_branch"] = "schoolapp.view_branch"
        return user.has_perm(switch.get(view.action, ""))


class BranchGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("schoolapp", "branch")
        return user.has_perm(switch.get(view.action, ""))


class LessonGetOrModifyPermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("classapp", "lesson")
        return user.has_perm(switch.get(view.action, ""))


class LessonGetOrModifyPermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("classapp", "lesson")
        return user.has_perm(switch.get(view.action, ""))


class RoomGetOrModifyPermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("classapp", "room")
        return user.has_perm(switch.get(view.action, ""))


class ClassGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        app_name = "classapp"
        model_name = "class"
        switch = generate_basic_permission_switch(app_name, model_name)
        switch["create_calendar"] = app_name + ".add_calendar"
        switch["list_calendar"] = app_name + ".view_calendar"
        switch["destroy_calendar"] = app_name + ".delete_calendar"
        switch["list_students"] = "studentapp.view_student"
        switch["create_student"] = "studentapp.add_student"
        switch["update_student"] = "studentapp.change_student"
        switch["list_exams"] = "classapp.view_exam"
        switch["create_exam"] = "classapp.add_exam"
        switch["destroy_exam"] = "classapp.delete_exam"
        switch["update_exam"] = "classapp.change_exam"
        return user.has_perm(switch.get(view.action, ""))


class CalendarGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("classapp", "calendar")
        return user.has_perm(switch.get(view.action, ""))


class StudentGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("studentapp", "student")
        switch["list_payments"] = "studentapp.view_payment"
        switch["create_payment"] = "studentapp.add_payment"
        switch["list_notes"] = "studentapp.view_note"
        switch["create_note"] = "studentapp.add_note"
        switch["create_journal"] = "studentapp.add_journal"
        switch["update_journal"] = "studentapp.change_journal"
        return user.has_perm(switch.get(view.action, ""))


class DatasheetGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("datasheetapp", "datasheet")
        return user.has_perm(switch.get(view.action, ""))


class DatasheetStatusGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("datasheetapp", "status")
        return user.has_perm(switch.get(view.action, ""))


class DiscountGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("studentapp", "discount")
        return user.has_perm(switch.get(view.action, ""))


class PaymentGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("studentapp", "payment")
        return user.has_perm(switch.get(view.action, ""))


class NoteGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("studentapp", "note")
        return user.has_perm(switch.get(view.action, ""))


class StatusGetOrModifySerializer(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("utilityapp", "status")
        return user.has_perm(switch.get(view.action, ""))


class PaymentMethodGetOrModifySerializer(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("utilityapp", "paymentmethod")
        return user.has_perm(switch.get(view.action, ""))
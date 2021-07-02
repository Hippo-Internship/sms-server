# Python imports
from datetime import datetime, timedelta
from re import M
# Django built-in imports
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
# Third party imports
from rest_framework.exceptions import PermissionDenied
# Local imports
from core.apps.studentapp import models as studentapp_models
from core.apps.datasheetapp import models as datasheetapp_models

# User model 
User = get_user_model()

def list_groups(user, queryset, filter_queries={}):
    print(user.groups.role_id)
    groups_switch = {
        User.SUPER_ADMIN: {},
        User.ADMIN: {
            "role_id__gt": User.ADMIN,
        },
        User.OPERATOR: {
            "role_id__gt": User.OPERATOR
        },
    }
    return queryset.filter(**groups_switch[user.groups.role_id])

def list_users(user, queryset, filter_queries={}):
    groups = filter_queries.pop("groups__role_id", None)
    if groups is None:
        return []
    if user.groups.role_id > groups:
        raise PermissionDenied()
    if user.groups.role_id == User.SUPER_ADMIN:
        users = queryset.filter(groups__role_id=groups, is_active=True, **filter_queries)
    elif user.groups.role_id == User.ADMIN:
        users = user.school.users.filter(groups__role_id=groups, is_active=True, **filter_queries)
    elif user.groups.role_id == User.OPERATOR:
        users = user.branch.users.filter(branch=user.branch, groups__role_id=groups, is_active=True, **filter_queries)
    else:
        return []
    return users

def generate_operator_profile_data(user: User):
    today_date = datetime.now()
    week_day = today_date.weekday()
    datasheets = user.registered_datasheets.all()
    students = user.registered_students.all()
    generated_data = {
        "user": user,
        "datasheet_count": [],
        "datasheet_total": datasheets.count(),
        "student_count": [],
        "student_total": students.count(),
        "register_statistics": generate_datasheet_by_register_type_data(user)
    }
    for day in range(week_day + 1):
        current_day = (today_date - timedelta(days=day)).strftime("%Y-%m-%d")
        d_count = datasheets.filter(created=current_day).count()
        s_count = students.filter(created=current_day).count()
        generated_data["datasheet_count"].append(d_count)
        generated_data["student_count"].append(s_count)
    return generated_data

def generate_teacher_student_data(user: User):
    today_date = datetime.now()
    # students = studentapp_models.Student.objects.filter(_class__teacher=user.id, is_active=False)
    students = studentapp_models.Student.objects.filter(canceled=False, _class__teacher=user.id)
    active_student_count = students.filter(end_date__gte=today_date).count()
    completed_student_count = students.filter(end_date__lt=today_date).count()
    generated_data = {
        "active_student_count": active_student_count,
        "completed_student_count": completed_student_count,
        "total": students.count()
    }
    return generated_data

def generate_teacher_class_data(user: User):
    today_date = datetime.now()
    classes = user.classes.all()
    active_class_count = classes.filter(end_date__gte=today_date, start_date__lte=today_date).count()
    finished_class_count = classes.filter(end_date__lt=today_date).count()
    active_class_count = classes.filter(start_date__gt=today_date).count()
    generated_data = {
        "active_class_count": active_class_count,
        "finished_class_count": finished_class_count,
        "active_class_count": active_class_count,
        "total": classes.count()
    }
    return generated_data

def generate_datasheet_by_register_type_data(user: User, filter_queries: dict={}, filter: int=1) -> dict:
    generated_data = user.registered_datasheets.aggregate(
        in_person_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.IN_PERSON)),
        phone_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.PHONE)),
        facebook_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.FACEBOOK)),
        instagram_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.INSTAGRAM)),
        website_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.WEBSITE)),
        other_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.OTHER)),
    )
    return generated_data
# Python imports
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# Django imports
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count, Min, Sum
from django.db.models.expressions import F
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
# Third party imports
# Local imports
from core.apps.studentapp import models as studentapp_models
from core.apps.classapp import models as classapp_models
from core.apps.utilityapp import models as utilityapp_models
from core.apps.schoolapp import models as schoolapp_models
from core.apps.datasheetapp import models as datasheetapp_models

User = get_user_model()

def generate_total_income_data(user: User, filter_queries: dict={}, filter: int=1, add_filter_queries: dict={}) -> dict:
    queryset: QuerySet = studentapp_models.Payment.objects
    class_queryset: QuerySet = classapp_models.Class.objects
    if user.groups.role_id == User.SUPER_ADMIN:
        payments = queryset.filter(**filter_queries)
        classes = class_queryset.filter(**add_filter_queries)
    elif user.groups.role_id == User.ADMIN:
        payments = queryset.filter(student__user__branch__school=user.school.id, **filter_queries)
        classes = class_queryset.filter(branch__school=user.school.id, **add_filter_queries)
    else:
        payments = queryset.filter(student__user__branch=user.branch, **filter_queries)
        classes = class_queryset.filter(branch=user.branch, **add_filter_queries)
    today_date = datetime.now()
    all_time_start_date = payments.aggregate(min_date=Min("date"))["min_date"]
    all_time_start_date = datetime(all_time_start_date.year, all_time_start_date.month, all_time_start_date.day) if all_time_start_date is not None else today_date
    income_by_filter: list = []
    income_dates: list = []
    total_income_by_filter: int = 0
    if filter == 1:
        for i in range(6, -1, -1):
            temp_date = today_date - timedelta(days=i)
            temp_income = payments.filter(date=temp_date).aggregate(income=Sum("paid"))
            real_income = temp_income["income"] if temp_income["income"] is not None else 0
            income_by_filter.append(real_income)
            total_income_by_filter += real_income
            income_dates.append(temp_date.strftime("%Y-%m-%d"))
        temp_total_lesson_price = classes.filter(start_date__range=[ today_date - timedelta(days=7), today_date ]).aggregate(total=Sum("lesson__price"))
    elif filter == 2:
        for i in range(12, 0, -1):
            temp_date = today_date - relativedelta(months=i - 1) 
            temp_income = payments.filter(
                date__range=[ 
                    today_date - relativedelta(months=i), 
                    temp_date
                ]).aggregate(income=Sum("paid"))
            real_income = temp_income["income"] if temp_income["income"] is not None else 0
            income_by_filter.append(real_income)
            total_income_by_filter += real_income
            income_dates.append(temp_date.strftime("%Y-%m-%d"))
        temp_total_lesson_price = classes.filter(start_date__range=[ today_date - relativedelta(months=12) , today_date ]).aggregate(total=Sum("lesson__price"))
    elif filter == 3:
        delta_days: int = (today_date.date() - all_time_start_date.date()).days
        _delta_days = int(delta_days / 12)
        remainder_days = delta_days - _delta_days * 12
        for i in range(12, 0, -1):
            temp_date = today_date - timedelta(days=(_delta_days * (i - 1)) + remainder_days if i - 1 != 0 else 0)  
            print("a", today_date - timedelta(days=(_delta_days * i) + remainder_days))
            print("b ", today_date - timedelta(days=(_delta_days * (i - 1)) + remainder_days if i - 1 != 0 else 0))
            temp_income = payments.filter(
                date__gt=today_date - timedelta(days=(_delta_days * i) + remainder_days), 
                date__lte=temp_date
            ).aggregate(income=Sum("paid"))
            real_income = temp_income["income"] if temp_income["income"] is not None else 0
            income_by_filter.append(real_income)
            total_income_by_filter += real_income
            income_dates.append(temp_date.strftime("%Y-%m-%d"))
        temp_total_lesson_price = classes.filter(start_date__range=[ today_date - timedelta(days=delta_days), today_date ]).aggregate(total=Sum("lesson__price"))
    temp_pending = temp_total_lesson_price["total"] if temp_total_lesson_price["total"] is not None else 0
    real_pending = temp_pending - total_income_by_filter
    generated_data: dict = {
        "income": {
            "total": total_income_by_filter,
            "data": income_by_filter,
            "dates": income_dates
        },
        "pending": real_pending
    }
    return generated_data

def generate_students_data(user, filter_queries: dict={}, filter: int=3) -> dict:
    queryset: QuerySet = User.objects
    if user.groups.role_id == User.SUPER_ADMIN:
        students = queryset.filter(groups__role_id=User.STUDENT, **filter_queries)
    elif user.groups.role_id == User.ADMIN:
        students = queryset.filter(groups__role_id=User.STUDENT, school=user.school.id, **filter_queries)
    else:
        students = queryset.filter(groups__role_id=User.STUDENT, branch=user.branch, **filter_queries)
    today_date = datetime.now()
    _students = studentapp_models.Student.objects.filter(
        user__in=students, 
        canceled=False
    )
    active_students = students.filter(
        students__end_date__gte=today_date, 
        students__canceled=False
    ).distinct()
    recurring_students = _students.values('user').annotate(cnt=Count('_class')).filter(cnt__gt = 1)
    total_graduates = _students.aggregate(count=Count("id", filter=Q(end_date__lte=today_date, end_date=F("_class__end_date"))))
    total_cancellation = studentapp_models.Student.objects.aggregate(count=Count("canceled", filter=Q(canceled=True)))
    generated_data: dict = {
        "active_students": active_students.count(),
        "recurring_students": recurring_students.count(),
        "total_students": students.count(),
        "total_graduates": total_graduates["count"],
        "total_cancellation": total_cancellation["count"]
    }
    return generated_data

def generate_payment_by_type_data(user, filter_queries: dict={}, filter: int=3) -> QuerySet:
    queryset: QuerySet = utilityapp_models.PaymentMethod.objects
    if user.groups.role_id == User.SUPER_ADMIN:
        payments = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        payments = queryset.filter(school=user.school.id, **filter_queries)
    else:
        payments = queryset.filter(branch=user.branch, **filter_queries)
    annotated_payments = payments.annotate(total=Sum("payments__paid")).order_by("branch")
    return annotated_payments

def generate_student_by_status_data(user, filter_queries: dict={}, filter: int=3) -> QuerySet:
    queryset: QuerySet = utilityapp_models.Status.objects
    if user.groups.role_id == User.SUPER_ADMIN:
        statuses = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        statuses = queryset.filter(school=user.school.id, **filter_queries)
    else:
        statuses = queryset.filter(branch=user.branch, **filter_queries)
    annotated_statuses = statuses.annotate(count=Count("students")).order_by("branch")
    return annotated_statuses

def generate_payment_by_branch_data(user, filter_queries: dict={}, filter: int=3) -> QuerySet:
    queryset: QuerySet = schoolapp_models.Branch.objects
    if user.groups.role_id == User.SUPER_ADMIN:
        branches = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        branches = queryset.filter(school=user.school.id, **filter_queries)
    annotated_branches = branches.annotate(total=Sum("payments__paid")).order_by("-total")[:5]
    return annotated_branches                              

def generate_payment_by_lesson_data(user, filter_queries: dict={}, filter: int=3) -> QuerySet:
    queryset: QuerySet = classapp_models.Lesson.objects
    if user.groups.role_id == User.SUPER_ADMIN:
        lessons = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        lessons = queryset.filter(branch__school=user.school.id, **filter_queries)
    else:
        lessons = queryset.filter(branch=user.branch, **filter_queries)
    annotated_lessons = lessons.annotate(total=Sum("classes__students__payments__paid")).order_by("total")
    return annotated_lessons

def generate_datasheet_data(user: User, filter_queries: dict={}, filter: int=1) -> dict:
    queryset: QuerySet = datasheetapp_models.Datasheet.objects
    if user.groups.role_id == User.SUPER_ADMIN:
        datasheets = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        datasheets = queryset.filter(branch__school=user.school.id, **filter_queries)
    else:
        datasheets = queryset.filter(branch=user.branch, **filter_queries)
    today_date = datetime.now()
    all_time_start_date = datasheets.aggregate(min_date=Min("created"))["min_date"]
    all_time_start_date = datetime(all_time_start_date.year, all_time_start_date.month, all_time_start_date.day) if all_time_start_date is not None else today_date
    count_by_filter: list = []
    count_dates: list = []
    total_count_by_filter: int = 0
    if filter == 1:
        for i in range(6, -1, -1):
            temp_date = today_date - timedelta(days=i)
            temp_count = datasheets.filter(created=temp_date).aggregate(count=Count("id"))
            real_count = temp_count["count"] if temp_count["count"] is not None else 0
            count_by_filter.append(real_count)
            total_count_by_filter += real_count
            count_dates.append(temp_date.strftime("%Y-%m-%d"))
    elif filter == 2:
        for i in range(12, 0, -1):
            temp_date = today_date - relativedelta(months=i - 1) 
            temp_count = datasheets.filter(
                created__range=[ 
                    today_date - relativedelta(months=i), 
                    temp_date
                ]).aggregate(count=Count("id"))
            real_count = temp_count["count"] if temp_count["count"] is not None else 0
            count_by_filter.append(real_count)
            total_count_by_filter += real_count
            count_dates.append(temp_date.strftime("%Y-%m-%d"))
    elif filter == 3:
        delta_days: int = (today_date.date() - all_time_start_date.date()).days
        gap = 12 if delta_days > 12 else 1
        _delta_days = int(delta_days / gap)
        remainder_days = delta_days - _delta_days * gap
        for i in range(gap, 0, -1):
            temp_date = today_date - timedelta(days=(_delta_days * (i - 1)) + remainder_days if i - 1 != 0 else 0)  
            temp_count = datasheets.filter(
                created__range=[ 
                    today_date - timedelta(days=(_delta_days * i) + remainder_days), 
                    temp_date
                ]).aggregate(count=Count("id"))
            real_count = temp_count["count"] if temp_count["count"] is not None else 0
            count_by_filter.append(real_count)
            total_count_by_filter += real_count
            count_dates.append(temp_date.strftime("%Y-%m-%d"))
    generated_data: dict = {
        "total": total_count_by_filter,
        "data": count_by_filter,
        "dates": count_dates
    }
    return generated_data

def generate_datasheet_by_operator_data(user, filter_queries: dict={}, filter: int=3) -> QuerySet:
    queryset: QuerySet = User.objects
    if user.groups.role_id == User.SUPER_ADMIN:
        operators = queryset.filter(groups__role_id=user.OPERATOR, **filter_queries)
    elif user.groups.role_id == User.ADMIN:
        operators = queryset.filter(groups__role_id=user.OPERATOR, school=user.school.id, **filter_queries)
    else:
        operators = queryset.filter(groups__role_id=user.OPERATOR, branch=user.branch, **filter_queries)
    annotated_operators = operators.annotate(datasheet_count=Count("registered_datasheets")).order_by("datasheet_count")
    return annotated_operators

def generate_datasheet_by_register_type_data(user: User, filter_queries: dict={}, filter: int=1) -> dict:
    queryset: QuerySet = datasheetapp_models.Datasheet.objects
    if user.groups.role_id == User.SUPER_ADMIN:
        datasheets = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        datasheets = queryset.filter(branch__school=user.school.id, **filter_queries)
    else:
        datasheets = queryset.filter(branch=user.branch, **filter_queries)
    generated_data = datasheets.aggregate(
        in_person_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.IN_PERSON)),
        phone_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.PHONE)),
        facebook_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.FACEBOOK)),
        instagram_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.INSTAGRAM)),
        website_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.WEBSITE)),
        other_count=Count("id", filter=Q(register_type=datasheetapp_models.Datasheet.OTHER)),
    )
    return generated_data
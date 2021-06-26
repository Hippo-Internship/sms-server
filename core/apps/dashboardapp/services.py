# Python imports
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# Django imports
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Min, Sum
from django.db.models.query import QuerySet
# Third party imports
# Local imports
from core.apps.studentapp import models as studentapp_models
from core.apps.classapp import models as classapp_models

User = get_user_model()

def generate_total_income_data(user: User, filter_queries: dict={}, filter: int=1) -> dict:
    queryset: QuerySet = studentapp_models.Payment.objects
    class_queryset: QuerySet = classapp_models.Class.objects
    if user.groups.role_id == User.SUPER_ADMIN:
        payments = queryset.filter(**filter_queries)
        classes = class_queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        payments = queryset.filter(student__user__branch__school=user.school.id, **filter_queries)
        classes = class_queryset.filter(branch__school=user.school.id, **filter_queries)
    else:
        payments = queryset.filter(student__user__branch=user.branch, **filter_queries)
        classes = class_queryset.filter(branch=user.branch, **filter_queries)
    all_time_start_date = classes.aggregate(min_date=Min("start_date"))["min_date"]
    all_time_start_date = datetime(all_time_start_date.year, all_time_start_date.month, all_time_start_date.day)
    income_by_filter: list = []
    income_dates: list = []
    total_income_by_filter: int = 0
    today_date = datetime.now()
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
            temp_income = payments.filter(
                date__range=[ 
                    today_date - timedelta(days=(_delta_days * i) + remainder_days), 
                    temp_date
                ]).aggregate(income=Sum("paid"))
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

    return 12
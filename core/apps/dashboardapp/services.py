# Python imports
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# Django imports
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Sum
from django.db.models.query import QuerySet
# Third party imports
# Local imports
from core.apps.studentapp import models as studentapp_models

User = get_user_model()

def generate_total_income_data(user: User, filter_queries: dict={}, filter: int=3) -> dict:
    queryset: QuerySet = studentapp_models.Payment.objects
    if user.groups.role_id == User.SUPER_ADMIN:
        payments = queryset.filter(**filter_queries)
        all_time_start_date = user.date_joined
    elif user.groups.role_id == User.ADMIN:
        payments = queryset.filter(student__user__branch__school=user.school.id, **filter_queries)
        all_time_start_date = user.school.created
    else:
        payments = queryset.filter(student__user__branch=user.branch, **filter_queries)
        all_time_start_date = user.branch.created
    income_by_filter: list = []
    income_dates: list = []
    total_income_by_filter: int = 0
    today_date = datetime.now()
    if filter == 1:
        for i in range(6, -1, -1):
            temp_date = today_date - today_date - timedelta(days=i)
            temp_income = payments.filter(date=temp_date).aggregate(income=Sum("paid"))
            real_income = temp_income["income"] if temp_income["income"] is not None else 0
            income_by_filter.append(real_income)
            total_income_by_filter += real_income
            income_dates.append(temp_date.strftime("%Y-%m-%d"))
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
    generated_data: dict = {
        "income": {
            "total": total_income_by_filter,
            "data": income_by_filter,
            "dates": income_dates
        },
    }
    print(generated_data)
    return generated_data
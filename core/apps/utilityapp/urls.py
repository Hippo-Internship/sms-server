# Django built-in imports
from django.urls import path
# Third party imports
from rest_framework.routers import DefaultRouter
# Local imports
from . import views as local_views


urlpatterns = [
    path("detail", local_views.ListDetailView.as_view(), name="detail-list")
]

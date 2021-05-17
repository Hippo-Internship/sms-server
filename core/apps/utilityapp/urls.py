# Django built-in imports
from django.db import router
from django.urls import path
# Third party imports
from rest_framework.routers import DefaultRouter
# Local imports
from . import views as local_views


router = DefaultRouter()
router.register("status", local_views.StatusViewSet, basename="status")
router.register("method", local_views.PaymentMethodViewSet, basename="payment_method")

urlpatterns = [
    path("detail", local_views.ListDetailView.as_view(), name="detail-list")
] + router.urls

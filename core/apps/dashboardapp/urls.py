# Django imports
from django.urls import path
# Third party imports
from rest_framework.routers import DefaultRouter
# Local imports
from . import views

router = DefaultRouter()
router.register("", views.DashboardViewset, "dashboard")

urlpatterns = router.urls
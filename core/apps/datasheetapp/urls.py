# Django built-in imports
from django.urls import path
# Third party imports
from rest_framework.routers import DefaultRouter
# Local imports
from . import views as local_views


router = DefaultRouter()
router.register("action", local_views.DatasheetViewSet, "datasheet")


urlpatterns = router.urls

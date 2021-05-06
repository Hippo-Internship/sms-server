# Django built-in imports
from django.urls import path
# Third party imports
from rest_framework.routers import DefaultRouter
# Local imports
from . import views as local_views


router = DefaultRouter()
router.register("lesson", local_views.LessonViewSet, basename="lesson")

urlpatterns = router.urls
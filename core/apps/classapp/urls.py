# Django built-in imports
from django.urls import path, include
# Third party imports
from rest_framework.routers import DefaultRouter
# Local imports
from . import views as local_views


router = DefaultRouter()
router.register("lesson", local_views.LessonViewSet, basename="lesson")
router.register("room", local_views.RoomViewSet, basename="room")
router.register("action", local_views.ClassViewSet, basename="class")

urlpatterns = router.urls
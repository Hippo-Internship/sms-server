# Django built-in imports
from django.urls import path
# Third Party imports
from rest_framework.routers import DefaultRouter
# Local imports
from . import views as local_views


router = DefaultRouter()
router.register("action", local_views.StudentViewSet, basename="student")
router.register("discount", local_views.DiscountViewSet, basename="discount")
router.register("payment", local_views.PaymentViewSet, basename="payment")
router.register("note", local_views.NoteViewSet, basename="note")

urlpatterns = router.urls
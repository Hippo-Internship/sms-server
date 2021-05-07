# Django imports
from django.urls import path, include
# Third party imports
from rest_framework.routers import DefaultRouter
# Local imports
from . import views as local_views

# Router
router = DefaultRouter()
router.register("action", local_views.UserViewSet, basename="actions")

urlpatterns = [
    path("", include("dj_rest_auth.urls"))
]

urlpatterns += router.urls

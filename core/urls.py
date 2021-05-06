from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include("core.apps.authapp.urls")),
    path("api/school/", include("core.apps.schoolapp.urls")),
]

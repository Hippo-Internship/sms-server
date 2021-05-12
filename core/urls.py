from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include("core.apps.authapp.urls")),
    path("api/school/", include("core.apps.schoolapp.urls")),
    path("api/class/", include("core.apps.classapp.urls")),
    path("api/student/", include("core.apps.studentapp.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

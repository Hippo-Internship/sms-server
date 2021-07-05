from django.apps import AppConfig


class SchoolappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.apps.schoolapp'

    def ready(self):
        import core.apps.schoolapp.signals
from django.apps import AppConfig


class ClassappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.apps.classapp'

    def ready(self):
        import core.apps.classapp.signals

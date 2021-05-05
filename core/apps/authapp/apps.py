from django.apps import AppConfig


class AuthappConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.apps.authapp'

    def ready(self):
        import core.apps.authapp.signals

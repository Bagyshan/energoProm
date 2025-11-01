from django.apps import AppConfig


class CheckConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'check'

    def ready(self):
        import check.signals
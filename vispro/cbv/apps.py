from django.apps import AppConfig


class CbvConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cbv'

    def ready(self):
        import cbv.signals


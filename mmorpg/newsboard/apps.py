from django.apps import AppConfig


class NewsboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsboard'

    def ready(self):
        import newsboard.signals
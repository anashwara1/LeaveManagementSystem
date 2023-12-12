from django.apps import AppConfig
from .tasks import start_scheduler


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        start_scheduler()

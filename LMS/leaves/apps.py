from django.apps import AppConfig
from .tasks import start_scheduler

class LeavesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leaves'

    def ready(self):
        start_scheduler()


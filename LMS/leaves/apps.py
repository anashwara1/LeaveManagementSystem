import os
from django.apps import AppConfig
from .tasks import start_scheduler



class LeavesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leaves'

    def ready(self):
        run_once = os.environ.get('run_already')
        if run_once is not None:
            return
        os.environ['run_already'] = 'True'
        start_scheduler()



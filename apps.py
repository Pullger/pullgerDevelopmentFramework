import os
from django.apps import AppConfig
from pullgerDevelopmentFramework import core


class PullgerDevelopmentFramework(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pullgerDevelopmentFramework'
    multi_session_manager = None

    def ready(self):
        self.development_framework = core.DevelopmentFrameworkManager()
        if os.environ.get('RUN_MAIN') == 'true':
            pass

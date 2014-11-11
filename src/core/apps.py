from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'core'
    verbose_name = 'Acotel Blacklist'

    def ready(self):
        # import signal handlers
        import core.signals.handlers

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        try:
            import uwsgidecorators
            from . import cronjobs
        except ImportError:
            pass


from django.apps import AppConfig


class FadderanmalanConfig(AppConfig):
    name = 'fadderanmalan'

    def ready(self):
        from . import signals

        try:
            import uwsgidecorators
            from . import cronjobs
        except ImportError:
            pass

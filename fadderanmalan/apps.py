from django.apps import AppConfig


class FadderanmalanConfig(AppConfig):
    name = 'fadderanmalan'

    def ready(self):
        from . import signals

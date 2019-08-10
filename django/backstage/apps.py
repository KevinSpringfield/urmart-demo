from django.apps import AppConfig


class BackstageConfig(AppConfig):
    name = 'backstage'

    def ready(self):
        import backstage.signals

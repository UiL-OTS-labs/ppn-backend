from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'api.auth'
    label = 'apiauth'

    def ready(self):
        import api.auth.signals  # NoQA

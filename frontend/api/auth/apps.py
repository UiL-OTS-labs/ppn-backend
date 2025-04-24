from django.apps import AppConfig

from cdh.rest.mixins import ClientResourceSetupMixin


class AuthConfig(ClientResourceSetupMixin, AppConfig):
    name = 'api.auth'
    label = 'apiauth'

from django.apps import AppConfig

from cdh.rest.mixins import ClientResourceSetupMixin


class ApiConfig(ClientResourceSetupMixin, AppConfig):
    name = 'api'

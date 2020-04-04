from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class ActivationConfig(AppConfig):
    name = 'activation'


class SuitConfig(DjangoSuitConfig):
    layout = "horizontal"

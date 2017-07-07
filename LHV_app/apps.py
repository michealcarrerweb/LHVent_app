from __future__ import unicode_literals

from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "LHV_app"

    def ready(self):
        import_module("LHV_app.receivers")

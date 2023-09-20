from django.apps import AppConfig
from django.contrib.admin.apps import SimpleAdminConfig


class FormulaAdminConfig(SimpleAdminConfig):
    default_site = "formula.sites.FormulaAdminSite"
    default = False

    def ready(self):
        super().ready()
        self.module.autodiscover()


class FormulaConfig(AppConfig):
    name = "formula"
    default = True

from django.apps import AppConfig


class FormulaAdminConfig(AppConfig):
    name = "formula"
    default = True

    def ready(self):
        import formula.signals  # NOQA

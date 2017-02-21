from django.apps import AppConfig


class GoConfig(AppConfig):
    name = 'texaslan.go'
    verbose_name = "Go"

    def ready(self):
        """Override this to put in:
        """
        pass

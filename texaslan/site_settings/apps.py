from django.apps import AppConfig


class SiteSettingsConfig(AppConfig):
    name = 'texaslan.site_settings'
    verbose_name = "Site Settings"

    def ready(self):
        """Override this to put in:
        """
        pass

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

VOTING_STATUS_CHOICES = (
    ("C", "Closed"),
    ("A", "Applications"),
    ("X", "Applications Closed"),
    ("V", "Voting"),
    ("D", "Done"),
)


class SiteSettings(models.Model):
    class Meta:
        verbose_name_plural = "Site Settings"

    is_rush_open = models.BooleanField(_("Is rush open"), default=False)
    voting_status = models.CharField(_("Voting Status"), max_length=1, choices=VOTING_STATUS_CHOICES, default="C")

    def __str__(self):
        return str(self.id)


class SiteSettingService():
    @staticmethod
    def get_site_settings():
        site_settings_list = list(SiteSettings.objects.filter(pk__gt=-1))
        if not site_settings_list:
            site_settings = SiteSettings.objects.create()
            site_settings.save()
            site_settings_list.append(site_settings)
        else:
            site_settings = site_settings_list[0]
        return site_settings

    @staticmethod
    def is_rush_open():
        return SiteSettingService.get_site_settings().is_rush_open

    @staticmethod
    def is_voting_closed():
        return SiteSettingService.get_site_settings().voting_status == 'C'

    @staticmethod
    def is_voting_applications_open():
        return SiteSettingService.get_site_settings().voting_status == 'A'

    @staticmethod
    def is_voting_application_closed():
        return SiteSettingService.get_site_settings().voting_status == 'X'

    @staticmethod
    def is_voting_currently():
        return SiteSettingService.get_site_settings().voting_status == 'V'

    @staticmethod
    def is_voting_done():
        return SiteSettingService.get_site_settings().voting_status == 'D'

    @staticmethod
    def set_voting_applications_open():
        site_setting = SiteSettingService.get_site_settings()
        site_setting.voting_status = 'A'
        site_setting.save()

    @staticmethod
    def set_voting_done():
        site_setting = SiteSettingService.get_site_settings()
        site_setting.voting_status = 'D'
        site_setting.save()

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
    def is_rush_open():
        site_settings = SiteSettings.objects.filter(pk__gt=-1)[0]
        if not site_settings:
            site_settings = SiteSettings.objects.create()
            site_settings.save()
        return site_settings.is_rush_open

    @staticmethod
    def is_voting_closed():
        site_settings = SiteSettings.objects.filter(pk__gt=-1)[0]
        if not site_settings:
            site_settings = SiteSettings.objects.create()
            site_settings.save()
        return site_settings.voting_status == 'C'

    @staticmethod
    def is_voting_applications_open():
        site_settings = SiteSettings.objects.filter(pk__gt=-1)[0]
        if not site_settings:
            site_settings = SiteSettings.objects.create()
            site_settings.save()
        return site_settings.voting_status == 'A'

    @staticmethod
    def is_voting_application_closed():
        site_settings = SiteSettings.objects.filter(pk__gt=-1)[0]
        if not site_settings:
            site_settings = SiteSettings.objects.create()
            site_settings.save()
        return site_settings.voting_status == 'X'

    @staticmethod
    def is_voting_currently():
        site_settings = SiteSettings.objects.filter(pk__gt=-1)[0]
        if not site_settings:
            site_settings = SiteSettings.objects.create()
            site_settings.save()
        return site_settings.voting_status == 'V'

    @staticmethod
    def is_voting_done():
        site_settings = SiteSettings.objects.filter(pk__gt=-1)[0]
        if not site_settings:
            site_settings = SiteSettings.objects.create()
            site_settings.save()
        return site_settings.voting_status == 'D'

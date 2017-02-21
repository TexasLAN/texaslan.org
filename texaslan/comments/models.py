from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Comment(models.Model):
    message = models.TextField(_("Message"), null=True, blank=True)
    is_open = models.BooleanField(_("Is Open"), default=True)

    def __str__(self):
        return str(self.id)

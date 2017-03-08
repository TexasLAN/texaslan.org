from django.core import validators
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Application(models.Model):
    question_1 = models.TextField(_("Question 1"), null=True, blank=True,
                                  help_text='Why do you want to rush Lambda Alpha Nu?')
    question_2 = models.TextField(_("Question 2"), null=True, blank=True,
                                  help_text='Talk about yourself in a couple of sentences.')
    question_3 = models.TextField(_("Question 3"), null=True, blank=True,
                                  help_text='What is your major and why did you choose it?')
    question_4 = models.TextField(_("Question 4"), null=True, blank=True,
                                  help_text='What do you do in your spare time?')
    question_5 = models.TextField(_("Question 5"), null=True, blank=True,
                                  help_text='Talk about a current event in technology and why it interests you.')
    question_6 = models.TextField(_("Question 6"), null=True, blank=True, help_text='Impress us.')
    question_7 = models.TextField(_("Question 7"), null=True, blank=True,
                                  help_text='If you were to work on a personal project this semester that you could put on your resume, what would it be? (ex: an iOS app that is Tinder for dogs)')
    applicant_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="applicant_user",
                                       verbose_name=_("Applicant"))
    is_submitted = models.BooleanField(_("Is Submitted"), default=False)

    def __str__(self):
        return str(self.id)


RATING_CHOICES = (
    (1, "Strong No"),
    (2, "Weak No"),
    (3, "Neutral"),
    (4, "Weak Yes"),
    (5, "Strong Yes"),
)


class Review(models.Model):
    comment = models.TextField(_("Comment"), null=True, blank=True)
    rating = models.SmallIntegerField(_("Rating"), default=3, choices=RATING_CHOICES)
    application = models.ForeignKey(Application, null=True, related_name="application",
                                    verbose_name=_("Application"))
    reviewer_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="reviewer_user",
                                      verbose_name=_("Reviewer"))

    def __str__(self):
        return str(self.application.id)

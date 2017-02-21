from django import forms
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _

from config.settings.common import EMAIL_WEBMASTER, DEFAULT_FROM_EMAIL
from texaslan.users.models import UserService
from texaslan.utils.utils import subscribe_to_newsletter


class NotifyForm(forms.Form):
    mailing_list = forms.ChoiceField(choices=(
        (0, _("Webmaster Test")),
        (1, _("Disabled")),
        (2, _("Open Rushie")),
        (3, _("Closed Rushie")),
        (4, _("Pledge")),
        (5, _("Active")),
        (6, _("Officer")),
        (7, _("Inactive")),
        (8, _("Alumni"))
    ))
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):

        email_to = []
        list_option = int(self.cleaned_data['mailing_list'])
        if list_option == 1:
            email_to = UserService.get_disabled_users_emails()
        elif list_option == 2:
            email_to = UserService.get_open_rushie_users_emails()
        elif list_option == 3:
            email_to = UserService.get_closed_rushie_users_emails()
        elif list_option == 4:
            email_to = UserService.get_pledge_users_emails()
        elif list_option == 5:
            email_to = UserService.get_active_users_emails()
        elif list_option == 6:
            email_to = UserService.get_officer_users_emails()
        elif list_option == 7:
            email_to = UserService.get_inactive_users_emails()
        elif list_option == 8:
            email_to = UserService.get_alumni_users_emails()
        else:
            email_to = [EMAIL_WEBMASTER]

        mail = EmailMessage(subject=self.cleaned_data['subject'],
                            body=self.cleaned_data['message'],
                            from_email=DEFAULT_FROM_EMAIL)
        mail.bcc = email_to
        mail.to = [DEFAULT_FROM_EMAIL]
        mail.send()
        pass


class NotifyMeForm(forms.Form):
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    def subscribe(self):
        subscribe_to_newsletter(self.cleaned_data['email'],
                                first_name=self.cleaned_data['first_name'],
                                last_name=self.cleaned_data['last_name'])
        pass

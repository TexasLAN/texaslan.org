from django import forms
from django.contrib.auth import get_user_model
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

from os import path

from .models import User
from texaslan.applications.models import Application


class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'nick_name', 'graduation_date', 'concentration', 'gender']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'nick_name': forms.TextInput(attrs={'placeholder': 'Nick Name'}),
            'graduation_date': forms.TextInput(attrs={'placeholder': 'Graduation Date'}),
        }

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.full_name = self.cleaned_data['full_name']
        user.nick_name = self.cleaned_data['nick_name']
        user.graduation_date = self.cleaned_data['graduation_date']
        user.save()

        open_rush_group = Group.objects.get(name="Open Rushie")
        open_rush_group.user_set.add(user)
        open_rush_group.save()

        (application, created) = Application.objects.get_or_create(applicant_user__pk=user.pk)
        application.applicant_user = user
        application.save()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'nick_name', 'graduation_date', 'concentration', 'gender']

# -*- coding: utf-8 -*-
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from texaslan.site_settings.models import SiteSettingService


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return SiteSettingService.is_rush_open()

    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data

        user.email = data.get('email')
        user.username = data.get('username')
        user.full_name = data.get('full_name')
        user.nick_name = data.get('nick_name')
        user.graduation_date = data.get('graduation_date')

        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return SiteSettingService.is_rush_open()

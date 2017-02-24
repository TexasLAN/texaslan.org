# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):
    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name', 'nick_name', 'graduation_date', 'concentration', 'gender',)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
                    ('User Profile', {'fields': (
                        'full_name', 'nick_name', 'graduation_date', 'concentration', 'gender', 'lan_class',)}),
                ) + AuthUserAdmin.fieldsets
    add_fieldsets = (
                        ('User Profile', {'fields': (
                            'full_name', 'nick_name', 'graduation_date', 'concentration', 'gender', 'lan_class',)}),
                    ) + AuthUserAdmin.fieldsets
    list_display = ('username', 'id', 'full_name', 'email', 'lan_class', 'graduation_date', 'is_superuser')
    search_fields = ['full_name']

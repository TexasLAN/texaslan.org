# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import hashlib

from django.contrib.auth.models import Group, AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("N", "Non - binary"),
    ("P", "Prefer not to answer")
)
CONCENTRATION_CHOICES = (
    ("CS", "Computer Science"),
    ("D", "Design"),
    ("B", "Business"),
    ("EE", "Electrical Engineering"),
    ("M", "Math"),
    ("MIS", "Management Information Systems"),
    ("O", "Other")
)
LAN_CLASS = (
    ("F", "Founder"),
    ("A", "Alpha"),
    ("B", "Beta"),
    ("G", "Gamma"),
    ("D", "Delta"),
    ("E", "Epsilon"),
    ("Z", "Zeta"),
)


@python_2_unicode_compatible
class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    graduation_date = models.DateField()
    concentration = models.CharField(max_length=3, choices=CONCENTRATION_CHOICES, default="O")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="P")
    lan_class = models.CharField(max_length=3, choices=LAN_CLASS, null=True, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_gravatar_image_url(self):
        return 'https://secure.gravatar.com/avatar/' + hashlib.md5(
            self.email.lower().encode('utf-8')).hexdigest() + '?s=200'

    def get_gender(self):
        for (short, actual) in GENDER_CHOICES:
            if short == self.gender:
                return actual
        return "N/A"

    def get_concentration(self):
        for (short, actual) in CONCENTRATION_CHOICES:
            if short == self.concentration:
                return actual
        return "N/A"

    # User Type

    def is_disabled(self):
        return not self.is_active

    def is_open_rushie(self):
        return self.groups.filter(name="Open Rushie").exists()

    def is_closed_rushie(self):
        return self.groups.filter(name="Closed Rushie").exists()

    def is_pledge(self):
        return self.groups.filter(name="Pledge").exists()

    def is_active_user(self):
        return self.groups.filter(name="Active").exists()

    def is_officer(self):
        return self.groups.filter(name="Officer").exists()

    def is_board(self):
        return self.groups.filter(name="Board").exists()

    def is_inactive(self):
        return self.groups.filter(name="Inactive").exists()

    def is_alumni(self):
        return self.groups.filter(name="Alumni").exists()


class UserService:
    # User Getters

    @staticmethod
    def get_disabled_users():
        return [user for user in User.objects.all() if user.is_disabled()]

    @staticmethod
    def get_open_rushie_users():
        return [user for user in User.objects.all() if user.is_open_rushie()]

    @staticmethod
    def get_closed_rushie_users():
        return [user for user in User.objects.all() if user.is_closed_rushie()]

    @staticmethod
    def get_pledge_users():
        return [user for user in User.objects.all() if user.is_pledge()]

    @staticmethod
    def get_active_users():
        return [user for user in User.objects.all() if user.is_active_user()]

    @staticmethod
    def get_officer_users():
        return [user for user in User.objects.all() if user.is_officer()]

    @staticmethod
    def get_board_users():
        return [user for user in User.objects.all() if user.is_board()]

    @staticmethod
    def get_inactive_users():
        return [user for user in User.objects.all() if user.is_inactive()]

    @staticmethod
    def get_alumni_users():
        return [user for user in User.objects.all() if user.is_alumni()]

    # Email Getters

    @staticmethod
    def get_disabled_users_emails():
        return [user.email for user in UserService.get_disabled_users()]

    @staticmethod
    def get_open_rushie_users_emails():
        return [user.email for user in UserService.get_open_rushie_users()]

    @staticmethod
    def get_closed_rushie_users_emails():
        return [user.email for user in UserService.get_closed_rushie_users()]

    @staticmethod
    def get_pledge_users_emails():
        return [user.email for user in UserService.get_pledge_users()]

    @staticmethod
    def get_active_users_emails():
        return [user.email for user in UserService.get_active_users()]

    @staticmethod
    def get_officer_users_emails():
        return [user.email for user in UserService.get_officer_users()]

    @staticmethod
    def get_board_users_emails():
        return [user.email for user in UserService.get_board_users()]

    @staticmethod
    def get_inactive_users_emails():
        return [user.email for user in UserService.get_inactive_users()]

    @staticmethod
    def get_alumni_users_emails():
        return [user.email for user in UserService.get_alumni_users()]

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the Home
    url(
        regex=r'^$',
        view=views.home_feed,
        name='feed'
    ),
]

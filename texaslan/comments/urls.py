# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the GoSetupView
    url(
        regex=r'^$',
        view=views.CommentView.as_view(),
        name='list'
    ),
]

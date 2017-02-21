# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=views.NotifyView.as_view(),
        name='notify'
    ),
    url(
        regex=r'^me/$',
        view=views.NotifyMeView.as_view(),
        name='me'
    ),
]

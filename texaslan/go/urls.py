# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the GoSetupView
    url(
        regex=r'^$',
        view=views.GoSetupView.as_view(),
        name='list'
    ),

    # URL pattern for the GoView
    url(
        regex=r'^(?P<go_id>[a-zA-Z0-9_-]+)/$',
        view=views.go,
        name='go'
    ),
]

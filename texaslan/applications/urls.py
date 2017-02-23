# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the Application
    url(
        regex=r'^modify/$',
        view=views.ApplicationModifyView.as_view(),
        name='modify'
    ),
    url(
        regex=r'^$',
        view=views.ApplicationListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^(?P<id>\d+)/$',
        view=views.ApplicationDetailView.as_view(),
        name='detail'
    ),
]

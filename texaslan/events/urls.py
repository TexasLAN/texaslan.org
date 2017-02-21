# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the Events
    url(
        regex=r'^$',
        view=views.EventListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^calendar/$',
        view=views.calendar,
        name='calendar'
    ),
    url(
        regex=r'^calendar/(?P<year>\d+)/(?P<month>\d+)/$',
        view=views.calendar,
        name='calendar'
    ),
    url(
        regex=r'^(?P<id>[\w.@+-]+)/$',
        view=views.EventDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^confirm/(?P<id>[\w.@+-]+)/(?P<username>[\w.@+-]+)/$',
        view=views.EventConfirmAttendanceView.as_view(),
        name='confirm'
    ),
]

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the GoSetupView
    url(
        regex=r'^$',
        view=views.CandidateListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^apply/(?P<position>[a-zA-Z0-9_-]+)/$',
        view=views.CandidateApplyView.as_view(),
        name='apply'
    ),
    url(
        regex=r'^candidate/(?P<position>[a-zA-Z0-9_-]+)/(?P<username>[\w.@+-]+)/$',
        view=views.CandidateDetailsView.as_view(),
        name='candidate_detail'
    ),
    url(
        regex=r'^vote/$',
        view=views.VoteView.as_view(),
        name='vote'
    ),
]

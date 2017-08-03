# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
                  url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
                  # Django Admin, use {% url 'admin:index' %}
                  url(settings.ADMIN_URL, include(admin.site.urls)),

                  # User management
                  url(r'^users/', include('texaslan.users.urls', namespace='users')),
                  url(r'^accounts/', include('allauth.urls')),

                  # Your stuff: custom urls includes go here
                  url(r'^events/', include('texaslan.events.urls', namespace='events')),
                  url(r'^', include('texaslan.home.urls', namespace='home')),
                  url(r'^go/', include('texaslan.go.urls', namespace='go')),
                  url(r'^notify/', include('texaslan.notify.urls', namespace='notify')),
                  url(r'^comments/', include('texaslan.comments.urls', namespace='comments')),
                  url(r'^applications/', include('texaslan.applications.urls', namespace='applications')),
                  url(r'^voting/', include('texaslan.voting.urls', namespace='voting')),
                  url(r'^photos/', include('texaslan.photos.urls', namespace='photos')),
                  url(r'^slack/', include('django_slack_oauth.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]

from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from .views import AuthRegisterUser, Status, Event
from ..users.models import User
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^jwt/login/', obtain_jwt_token),
    url(r'^jwt/refresh/', refresh_jwt_token),
    url(r'^jwt/verify/', verify_jwt_token),
    url(r'^jwt/register/', AuthRegisterUser.as_view()),
    url(r'^status/rush/', Status.as_view()),
    url(r'^events/', Event.as_view()),
]

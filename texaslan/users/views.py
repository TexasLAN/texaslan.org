# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from texaslan.utils.utils import MemberRequiredMixin, SelfOrMemberRequiredMixin
from .forms import UserUpdateForm
from .models import User

from django_slack_oauth.models import SlackOAuthRequest


class UserDetailView(SelfOrMemberRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Your profile was successfully saved!')
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['slack_auth'] = SlackOAuthRequest.objects.get(associated_user=self.request.user)
        except SlackOAuthRequest.DoesNotExist:
            data['slack_auth'] = None
        
        return data


class UserListView(MemberRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'



def delete_slack_token(request):
    slack_auth = get_object_or_404(SlackOAuthRequest, associated_user=request.user).delete()
    return HttpResponseRedirect(reverse('users:update'))


from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from config.settings.common import SENDGRID_API_KEY
from texaslan.events.models import Event, EventTag
from texaslan.voting.models import Candidate, VoteStatus
from texaslan.site_settings.models import SiteSettingService

import json
import sendgrid


class OfficerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_anonymous and self.request.user.is_officer()

    def handle_no_permission(self):
        if not self.request.user.is_anonymous:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class ActiveRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_anonymous and self.request.user.is_active_user()

    def handle_no_permission(self):
        if not self.request.user.is_anonymous:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class OpenRushieRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_anonymous and self.request.user.is_open_rushie()

    def handle_no_permission(self):
        if not self.request.user.is_anonymous:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class SelfOrMemberRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        is_self = self.kwargs.get("username") == self.request.user.username
        return not self.request.user.is_anonymous and (is_self or
                                                       self.request.user.is_active_user() or self.request.user.is_alumni())

    def handle_no_permission(self):
        if not self.request.user.is_anonymous:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class MemberRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_anonymous and (
            self.request.user.is_active_user() or self.request.user.is_alumni())

    def handle_no_permission(self):
        if not self.request.user.is_anonymous:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class EventPermissionsRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            event = Event.objects.get(id=self.kwargs.get("id"))
        except Event.DoesNotExist:
            return False

        user = self.request.user

        if user.is_anonymous or user.is_open_rushie():
            return event.is_open_rush_safe()
        elif user.is_closed_rushie():
            return event.is_closed_rush_safe()
        else:
            return True

    def handle_no_permission(self):
        if not self.request.user.is_anonymous:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class HasNotAppliedRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_anonymous:
            return False

        if not SiteSettingService.is_voting_applications_open():
            return False

        has_not_applied_yet = True
        try:
            Candidate.objects.get(position=self.kwargs.get("position"), user__username=self.request.user.username)
            has_not_applied_yet = False
        except Candidate.DoesNotExist:
            pass
        return self.request.user.is_active_user() and has_not_applied_yet

    def handle_no_permission(self):
        if not self.request.user.is_anonymous:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class HasNotVotedRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_anonymous:
            return False

        if not SiteSettingService.is_voting_currently():
            return False

        has_not_voted_yet = True
        try:
            vote_status = VoteStatus.objects.get(voter__username=self.request.user.username)
            has_not_voted_yet = not vote_status.has_voted
        except VoteStatus.DoesNotExist:
            # Not allowed to vote
            return False
        return self.request.user.is_active_user() and has_not_voted_yet

    def handle_no_permission(self):
        if not self.request.user.is_anonymous:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


def subscribe_to_newsletter(email, first_name, last_name):
    # sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    #
    # # Create/Find Sendgrid Recipient ID
    # data = [
    #     {
    #         "email": email,
    #         "first_name": first_name,
    #         "last_name": last_name
    #     }
    # ]
    # response = sg.client.contactdb.recipients.post(request_body=data)
    # body_json = json.loads(response.body.decode('utf-8'))
    #
    # recipient_id = body_json['persisted_recipients'][0]
    #
    # # Put Sendgrid Recipient ID into mailing list
    # sg.client.contactdb.lists._(SENDGRID_MAILING_LIST_ID).recipients._(recipient_id).post()
    pass


def subscribe_user_to_newsletter(user):
    # name_list = user.full_name.split()
    # first_name = name_list[0]
    # last_name = name_list[1] if len(name_list) > 1 else ""
    # subscribe_to_newsletter(user.email, first_name, last_name)
    pass


def unsubscribe_user_to_newsletter(email):
    # sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    #
    # # Find Recipient Sendgrid ID
    # response = sg.client.contactdb.recipients.search.get(query_params={'email': email})
    # body_json = json.loads(response.body.decode('utf-8'))
    # print(response.body)
    # print(response.status_code)
    #
    # # Remove Sendgrid Recipient ID from mailing list
    # recipient_id = body_json['recipients'][0]['id']
    # sg.client.contactdb.lists._(SENDGRID_MAILING_LIST_ID).recipients._(recipient_id).delete()
    pass

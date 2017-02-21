from django import forms
from django.shortcuts import get_object_or_404

from .models import Event
from ..users.models import User


class ConfirmAttendanceForm(forms.Form):
    def confirm_attendance(self):
        print(self.data)
        event_id = int(self.data['event_id'])
        username = self.data['username']

        event = get_object_or_404(Event, pk=event_id)
        user = get_object_or_404(User, username=username)
        event.attendees.add(user)
        pass

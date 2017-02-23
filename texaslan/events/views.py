import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView, FormView

from texaslan.utils.utils import OfficerRequiredMixin
from .forms import ConfirmAttendanceForm
from .models import Event, EventCalendar, EventTag
from ..users.models import User


class EventListView(ListView):
    model = Event
    # These next two lines tell the view to index lookups by username
    slug_field = 'startTime'
    slug_url_kwarg = 'startTime'

    def get_queryset(self):
        qs = super(EventListView, self).get_queryset()
        now = datetime.datetime.now()
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        qs = qs.filter(start_time__gte=now)

        tags = EventTag.objects.all()
        open_tag = [tag.id for tag in tags.filter(name="Open Rush")]
        closed_tag = [tag.id for tag in tags.filter(name="Closed Rush")]

        if self.request.user.is_anonymous() or self.request.user.is_open_rushie():
            qs = qs.filter(event_tags__in=open_tag)
        elif self.request.user.is_closed_rushie():
            qs = qs.filter(event_tags__in=closed_tag)

        return qs


def calendar(request, year=datetime.datetime.now().year, month=datetime.datetime.now().month):
    # setup arguments, as it is a string and needs to be an int
    year = int(year)
    month = int(month)

    event_list = Event.objects.order_by('start_time').filter(start_time__year=year, start_time__month=month)

    if request.user.is_anonymous() or request.user.is_open_rushie():
        event_list = [event for event in event_list if event.is_open_rush_safe()]
    elif request.user.is_closed_rushie():
        event_list = [event for event in event_list if event.is_closed_rush_safe()]
    else:
        event_list = [event for event in event_list if event.is_member_and_pledge_safe()]

    calendar_html = EventCalendar(event_list).formatmonth(year, month)

    data = {
        'calendar': mark_safe(calendar_html)
    }
    return render(request, 'events/event_calendar.html', context=data)


class EventDetailView(DetailView):
    model = Event
    slug_field = 'id'
    slug_url_kwarg = 'id'


class EventConfirmAttendanceView(OfficerRequiredMixin, FormView):
    template_name = 'events/event_confirm_attendance.html'
    form_class = ConfirmAttendanceForm

    def get_context_data(self, **kwargs):
        context = super(EventConfirmAttendanceView, self).get_context_data(**kwargs)
        id = int(self.kwargs.get("id"))
        context['event'] = get_object_or_404(Event, pk=id)
        context['user'] = get_object_or_404(User, username=self.kwargs.get("username"))
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.confirm_attendance()
        return super(EventConfirmAttendanceView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Confirmed!')
        return reverse('home:feed')

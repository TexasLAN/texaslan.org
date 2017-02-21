import datetime

from django.template import loader
from django.shortcuts import render

from texaslan.events.models import Event


# Create your views here.
def home_feed(request):
    now = datetime.datetime.now()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    event_list = Event.objects.order_by('start_time').filter(start_time__gte=now)

    if request.user.is_anonymous() or request.user.is_open_rushie():
        event_list = [event for event in event_list if event.is_open_rush_safe()]
    elif request.user.is_closed_rushie():
        event_list = [event for event in event_list if event.is_closed_rush_safe()]
    else:
        event_list = [event for event in event_list if event.is_member_and_pledge_safe()]

    data = {
        'event_list': event_list,
    }

    return render(request, 'home/home_feed.html', context=data)

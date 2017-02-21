from calendar import HTMLCalendar, SUNDAY, month_name
from datetime import date
from itertools import groupby

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import conditional_escape as esc
from django.utils.translation import ugettext_lazy as _


class EventTag(models.Model):
    name = models.CharField(_("Name"), max_length=255, null=False, blank=False, unique=True)
    def __str__(self):
        return self.name

class Event(models.Model):
    start_time = models.DateTimeField(_("Start Time"))
    end_time = models.DateTimeField(_("End Time"))
    title = models.CharField(_("Title"), max_length=255)
    location = models.CharField(_("Location"), max_length=255)
    description = models.TextField(_("Description"), null=True, blank=True)
    image_url = models.CharField(_("Image URL"), max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="event_creator",
                                verbose_name=_("Creator"))
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    event_tags = models.ManyToManyField(EventTag, related_name="event_tags", verbose_name=_("Tags"))
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="event_attendees",
                                       verbose_name=_("Attendees"))

    speaker_bio = models.TextField(null=True, blank=True)
    presented_by = models.CharField(null=True, blank=True, max_length=256)
    speaker = models.CharField(null=True, blank=True, max_length=256)

    def __str__(self):
        return self.title

    def is_open_rush_safe(self):
        return self.event_tags.filter(name="Open Rush").exists()

    def is_closed_rush_safe(self):
        return self.event_tags.filter(name="Closed Rush").exists()

    def is_member_and_pledge_safe(self):
        return True


class EventCalendar(HTMLCalendar):
    day_abbr = ["M", "T", "W", "T", "F", "S", "S"]

    def __init__(self, events):
        super(EventCalendar, self).__init__(SUNDAY)
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = ['<ul>']
                for event in self.events[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % reverse('events:detail', args={event.id}))
                    body.append(esc(event.title))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        self.year, self.month = theyear, themonth
        v = []
        a = v.append
        a('<table class="calendar">')
        a('\n<thead>\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n</thead>\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def group_by_day(self, events):
        field = lambda event: event.start_time.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="day %s">%s</td>' % (cssclass, body)

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return '<td class="header-day">%s</td>' % (self.day_abbr[day])

    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return '<tr class="header-days">%s</tr>' % s

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        <tr class="controls">
                <td class="clndr-previous-button">‹</td>
                <td class="current-month" colspan="5"><h3>August 2016</h3></td>
                <td class="clndr-next-button">›</td>
            </tr>
        """
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]

        v = []
        a = v.append
        a('<tr class="controls">')
        if themonth == 1:
            back_month = 12
            back_year = theyear - 1
        else:
            back_month = themonth - 1
            back_year = theyear
        a('<td class="clndr-previous-button"><a href="%s">‹</a></td>' % reverse('events:calendar',
                                                                                kwargs={'year': back_year,
                                                                                        'month': back_month}))
        a('<td colspan="5" class="current-month">%s</td>' % s)
        if themonth == 12:
            forward_month = 1
            forward_year = theyear + 1
        else:
            forward_month = themonth + 1
            forward_year = theyear
        a('<td class="clndr-next-button"><a href="%s">›</a></td>' % reverse('events:calendar',
                                                                            kwargs={'year': forward_year,
                                                                                    'month': forward_month}))
        a('</tr>')
        return ''.join(v)

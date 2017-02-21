from django.contrib import admin

from .models import Event, EventTag

@admin.register(EventTag)
class EventTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'creator', 'start_time', 'end_time')
    list_filter = ('creator',)
    ordering = ('-start_time',)

from django.contrib import admin

from .models import Application, Review


@admin.register(Application)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('applicant_user',)
    ordering = ('applicant_user',)

@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('application','reviewer_user','rating')
    ordering = ('application',)

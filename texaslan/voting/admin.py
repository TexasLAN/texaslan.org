from django.contrib import admin

from .models import Candidate, VoteBallot, VoteStatus


@admin.register(Candidate)
class VoteCandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'user', 'has_won')
    ordering = ('position',)


@admin.register(VoteBallot)
class VoteBallotAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'candidates_json')


@admin.register(VoteStatus)
class VoteStatusAdmin(admin.ModelAdmin):
    list_display = ('voter', 'has_voted',)

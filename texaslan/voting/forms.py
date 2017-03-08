from django import forms
from django.core.exceptions import ValidationError
import json

from .models import Candidate, VoteService, VoteStatus, CANDIDATE_POSITIONS, VoteBallot
from texaslan.site_settings.models import SiteSettingService


class StartElectionForm(forms.Form):
    def clean(self):
        success = VoteService.run_election()
        if not success:
            raise ValidationError('Runoff Election is required!')


class CreateCandidateApplicationForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['description', ]


class VoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        extra = kwargs.pop('extra')
        super(VoteForm, self).__init__(*args, **kwargs)

        for (position_id, position, candidates) in extra:
            choices = [(-1, "------")]
            for candidate in candidates:
                choices.append((candidate.id, candidate.user.full_name,))

            for i, candidate in enumerate(candidates):
                self.fields[position_id + '_' + str(i)] = forms.ChoiceField(choices=choices)
                if i == 0:
                    self.fields[position_id + '_' + str(i)].help_text = position

    def clean(self):
        # Check if voting is open
        if not SiteSettingService.is_voting_currently():
            raise forms.ValidationError("Voting is not open!")

        # Check if user hasn't already voted
        vote_status_query = VoteStatus.objects.filter(voter__username=self.user.username)
        if len(vote_status_query) != 0 and vote_status_query[0].has_voted:
            raise forms.ValidationError("You have already voted!")

        # Check if inputs are valid
        for (position_id, position_str) in CANDIDATE_POSITIONS:
            num_position_cand = len(Candidate.objects.filter(position=position_id))
            candidate_position_set = set()
            has_voted_none = False

            for i in range(num_position_cand):
                form_tag = position_id + '_' + str(i)
                candidate_id = int(self.cleaned_data[form_tag])
                if (has_voted_none and candidate_id != -1) or candidate_id in candidate_position_set:
                    raise forms.ValidationError("You filled your vote ballet wrong in the %s section!" % position_str)
                if candidate_id == -1:
                    has_voted_none = True
                else:
                    candidate_position_set.update({int(self.cleaned_data[form_tag])})

        return self.cleaned_data

    def submit_ballot(self, user):
        vote_status_query = VoteStatus.objects.filter(voter__username=self.user.username)
        status = vote_status_query[0]
        status.has_voted = True
        status.save()

        for (position_id, position_str) in CANDIDATE_POSITIONS:
            num_position_cand = len(Candidate.objects.filter(position=position_id))
            candidate_position_list = []

            for i in range(num_position_cand):
                form_tag = position_id + '_' + str(i)
                candidate_id = int(self.cleaned_data[form_tag])
                if candidate_id == -1:
                    break
                candidate_position_list.append(candidate_id)

            ballot = VoteBallot.objects.create()
            ballot.position = position_id
            ballot.candidates_json = json.dumps(candidate_position_list)
            ballot.save()

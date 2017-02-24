from django import forms
from django.core.exceptions import ValidationError
from .models import Candidate, VoteService


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
        extra = kwargs.pop('extra')
        super(VoteForm, self).__init__(*args, **kwargs)

        for (position_id, position, candidates) in extra:
            choices = []
            for candidate in candidates:
                choices.append((candidate.id, candidate.user.full_name,))

            for i, candidate in enumerate(candidates):
                self.fields[position_id + '_' + str(i)] = forms.IntegerField(choices=choices)
                if i == 0:
                    self.fields[position_id + '_' + str(i)].help_text = position

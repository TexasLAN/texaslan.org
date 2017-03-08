from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.forms import ValidationError

from .models import Candidate, VoteBallot, CANDIDATE_POSITIONS, VoteService, VoteStatus, POSITION_NUMS
from .forms import StartElectionForm, CreateCandidateApplicationForm, VoteForm
from texaslan.utils.utils import ActiveRequiredMixin, HasNotAppliedRequiredMixin, HasNotVotedRequiredMixin
from texaslan.site_settings.models import SiteSettingService


class CandidateListView(ActiveRequiredMixin, FormView):
    template_name = 'voting/candidate_list.html'
    form_class = StartElectionForm

    def get_context_data(self, **kwargs):
        context = super(CandidateListView, self).get_context_data(**kwargs)

        context['voting_closed'] = SiteSettingService.is_voting_closed()
        if context['voting_closed']:
            return context

        context['voting_open'] = SiteSettingService.is_voting_currently()

        context['has_not_voted'] = True
        try:
            vote_status = VoteStatus.objects.get(voter__username=self.request.user.username)
            context['has_not_voted'] = not vote_status.has_voted
        except VoteStatus.DoesNotExist:
            pass

        positions_list = []
        for (position_code, position_name) in CANDIDATE_POSITIONS:
            has_winner = False
            has_applied = False
            is_applying_open = SiteSettingService.is_voting_applications_open()
            try:
                list = Candidate.objects.filter(position=position_code)
                for cand in list:
                    if cand.user.pk == self.request.user.pk:
                        has_applied = True
                    if cand.has_won:
                        has_winner = True
            except Candidate.DoesNotExist:
                list = []
            positions_list.append((position_name, position_code, has_winner, has_applied, is_applying_open, list,))
        context['positions'] = positions_list
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Election was successful!')
        return reverse('voting:list')


class CandidateApplyView(HasNotAppliedRequiredMixin, CreateView):
    template_name = 'voting/candidate_apply.html'
    model = Candidate
    form_class = CreateCandidateApplicationForm

    def get_context_data(self, **kwargs):
        context = super(CandidateApplyView, self).get_context_data(**kwargs)
        context['position_id'] = self.kwargs.get("position")
        context['position'] = VoteService.get_position_str(context['position_id'])
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        candidate = form.instance
        candidate.position = form.data['position_id']
        candidate.user = self.request.user
        return super(CandidateApplyView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Application was submitted!')
        return reverse('voting:list')


class CandidateDetailsView(ActiveRequiredMixin, DetailView):
    template_name = 'voting/candidate_detail.html'
    model = Candidate

    def get_context_data(self, **kwargs):
        context = super(CandidateDetailsView, self).get_context_data(**kwargs)
        context['position_id'] = self.kwargs.get("position")
        context['position'] = VoteService.get_position_str(context['position_id'])
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Candidate,
                                 position=self.kwargs.get('position'), user__username=self.kwargs.get('username'))


class VoteView(HasNotVotedRequiredMixin, FormView):
    template_name = 'voting/vote.html'
    form_class = VoteForm

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors.as_data()['__all__'][0].message)
        return super(VoteView, self).form_invalid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Successfully voted!')
        return reverse('voting:list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.submit_ballot(self.request.user)
        return super(VoteView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(VoteView, self).get_form_kwargs()
        extra = []
        for (position_id, position) in CANDIDATE_POSITIONS:
            # If we have all our winners, no need to fill this out.
            if len(set(Candidate.objects.filter(position=position_id, has_won=True))) == POSITION_NUMS[position_id]:
                continue
            extra.append((position_id, position, set(Candidate.objects.filter(position=position_id)),))
        kwargs['extra'] = extra
        kwargs['user'] = self.request.user
        return kwargs

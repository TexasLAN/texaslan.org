from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.views.generic import FormView, UpdateView, ListView, TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ApplicationForm, ReviewForm
from .models import Application, Review
from texaslan.utils.utils import OpenRushieRequiredMixin, ActiveRequiredMixin
from texaslan.users.models import User
from texaslan.events.models import Event


class ApplicationModifyView(OpenRushieRequiredMixin, UpdateView):
    template_name = 'applications/applications_form.html'
    form_class = ApplicationForm

    def get_object(self, queryset=None):
        (application, created) = Application.objects.get_or_create(applicant_user__pk=self.request.user.id)
        application.applicant_user = self.request.user
        return application

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors.as_data()['__all__'][0].message)
        return super(ApplicationModifyView, self).form_invalid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Successfully saved application!')
        return reverse('applications:modify')


class ApplicationListView(ActiveRequiredMixin, TemplateView):
    template_name = 'applications/applications_list.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationListView, self).get_context_data(**kwargs)

        application_list = Application.objects.all()
        review_list = []
        avg_rating_list = []
        board_avg_rating_list = []
        anon_avg_rating_list = []
        for application in application_list:
            reviews = Review.objects.filter(application__pk=application.pk)
            avg_rating_total = 0
            avg_rating_count = 0
            board_avg_rating_total = 0
            board_avg_rating_count = 0
            rating_count = len(reviews)

            for review in reviews:
                if review.rating is None or review.reviewer_user is None:
                    continue

                avg_rating_count += 1
                avg_rating_total += review.rating
                
                if review.reviewer_user.is_board():
                    board_avg_rating_count += 1
                    board_avg_rating_total += review.rating

            if avg_rating_count != 0:
                avg_rating_list.append("{0:.2f}".format(avg_rating_total / avg_rating_count))
            else:
                avg_rating_list.append("-")

            if board_avg_rating_count != 0:
                board_avg_rating_list.append("{0:.2f}".format(board_avg_rating_total / board_avg_rating_count))
            else:
                board_avg_rating_list.append("-")
            
            try:
                Review.objects.get(application__pk=application.pk, reviewer_user__pk=self.request.user.pk)
                review_list.append(True)
            except Review.DoesNotExist:
                review_list.append(False)

        context['application_list'] = zip(application_list, review_list, avg_rating_list, board_avg_rating_list, rating_count)
        return context


class ApplicationDetailView(ActiveRequiredMixin, FormView):
    template_name = 'applications/applications_detail.html'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        app_id = int(self.kwargs.get("id"))
        context['application'] = get_object_or_404(Application, pk=app_id)
        context['rushie'] = context['application'].applicant_user

        reviews = Review.objects.filter(application__pk=app_id)
        member_avg_rating_total = 0
        member_avg_rating_count = 0
        board_avg_rating_total = 0
        board_avg_rating_count = 0
        anon_avg_rating_total = 0
        anon_avg_rating_count = 0

        for review in reviews:
            if review.rating is None:
                continue
            
            if review.reviewer_user is None:
                anon_avg_rating_count += 1
                anon_avg_rating_total += review.rating
            elif review.reviewer_user.is_board():
                board_avg_rating_count += 1
                board_avg_rating_total += review.rating
            else:
                member_avg_rating_count += 1
                member_avg_rating_total += review.rating

        avg_rating_total = member_avg_rating_total + board_avg_rating_total
        avg_rating_count = member_avg_rating_count + board_avg_rating_count

        if avg_rating_count != 0:
            context['avg_rating'] = "{0:.2f}".format(avg_rating_total / avg_rating_count)
        else:
            context['avg_rating'] = "-"

        if member_avg_rating_count != 0:
            context['member_avg_rating'] = "{0:.2f}".format(member_avg_rating_total / member_avg_rating_count)
        else:
            context['member_avg_rating'] = "-"

        if board_avg_rating_count != 0:
            context['board_avg_rating'] = "{0:.2f}".format(board_avg_rating_total / board_avg_rating_count)
        else:
            context['board_avg_rating'] = "-"

        if anon_avg_rating_count != 0:
            context['anon_avg_rating'] = "{0:.2f}".format(anon_avg_rating_total / anon_avg_rating_count)
        else:
            context['anon_avg_rating'] = "-"

        context['reviews'] = reviews
        context['events'] = list(context['rushie'].event_attendees.all())
        print(context['events'])
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.modify_review()
        return super(ApplicationDetailView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Confirmed!')
        return reverse('applications:list')

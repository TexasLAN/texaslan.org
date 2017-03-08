from django import forms
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Application, Review
from texaslan.users.models import User
from texaslan.site_settings.models import SiteSettingService


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6', 'question_7']

    def clean(self):
        application = self.save(commit=False)
        # This will validate if forms can be submitted or not

        if application.is_submitted:
            raise forms.ValidationError("Applications was already submitted")

        if not SiteSettingService.is_rush_open():
            raise forms.ValidationError("Applications is late")

        if 'submit_btn' in self.data:
            application.is_submitted = True


RATING_CHOICES = (
    (1, "Strong No"),
    (2, "Weak No"),
    (3, "Neutral"),
    (4, "Weak Yes"),
    (5, "Strong Yes"),
)


class ReviewForm(forms.ModelForm):
    is_anon_comment = forms.BooleanField(label="Is anonymous comment?", required=False)

    class Meta:
        model = Review
        fields = ['comment', 'rating']

    def modify_review(self):
        print(self.data)
        if "is_anon_comment" not in self.data or self.data["is_anon_comment"] == 'off':
            application_id = int(self.data['application_id'])
            username = self.data['review_username']
            comment = self.cleaned_data['comment']
            rating = self.cleaned_data['rating']

            application = get_object_or_404(Application, pk=application_id)
            reviewer = get_object_or_404(User, username=username)
            try:
                review = Review.objects.get(application__pk=application_id, reviewer_user__pk=reviewer.pk)
            except Review.DoesNotExist:
                review = Review.objects.create()
            review.rating = rating
            review.comment = comment
            review.application = application
            review.reviewer_user = reviewer
            review.save()
        else:
            anon_review = Review.objects.create()
            anon_review.rating = None
            anon_review.comment = self.cleaned_data['comment']
            anon_review.application = get_object_or_404(Application, pk=int(self.data['application_id']))
            anon_review.save()
        pass

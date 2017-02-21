from django import forms
from .models import Comment


class CommentForm(forms.Form):

    message = forms.CharField(widget=forms.Textarea)

    def create_comment(self):
        new_comment = Comment()
        new_comment.message = self.cleaned_data['message']
        new_comment.is_open = True
        new_comment.save()
        pass

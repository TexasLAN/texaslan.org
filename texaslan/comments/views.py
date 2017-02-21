from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from .forms import CommentForm
from .models import Comment
from texaslan.utils.utils import ActiveRequiredMixin


class CommentView(ActiveRequiredMixin, FormView):
    template_name = 'comments/comments_list.html'
    form_class = CommentForm
    success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        context = super(CommentView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        return context

    def form_valid(self, form):
        form.create_comment()
        return super(CommentView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Successfully created the comment!')
        return reverse('comments:list')

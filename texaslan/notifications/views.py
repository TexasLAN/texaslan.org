from django.views.generic import TemplateView

from texaslan.utils.utils import LoggedInRequiredMixin

class NotificationsView(LoggedInRequiredMixin, TemplateView):
    template_name = 'notifications/notifications_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data
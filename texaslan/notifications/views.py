from django.conf import settings
from django.views.generic import TemplateView

from texaslan.utils.utils import MemberRequiredMixin

class NotificationsView(MemberRequiredMixin, TemplateView):
    template_name = 'notifications/notifications_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # data['photos_folder_id'] = settings.PHOTOS_DRIVE_FOLDER_ID
        
        return data
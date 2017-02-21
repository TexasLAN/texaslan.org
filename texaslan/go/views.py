from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.views.generic import ListView

from .models import Go
from texaslan.utils.utils import OfficerRequiredMixin


class GoSetupView(OfficerRequiredMixin, ListView):
    model = Go


def go(request, go_id):
    go = get_object_or_404(Go, pk__iexact=go_id)
    return HttpResponseRedirect(go.url)

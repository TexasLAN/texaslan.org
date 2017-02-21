from django.contrib import admin

from .models import Go
from .forms import GoAdminForm
@admin.register(Go)
class GoAdmin(admin.ModelAdmin):
    form = GoAdminForm
    list_display = ('id', 'url')

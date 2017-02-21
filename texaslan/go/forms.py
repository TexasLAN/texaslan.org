from django import forms
from django.core.exceptions import ValidationError
from .models import Go
class GoAdminForm(forms.ModelForm):
    def clean_id(self):
        id = self.cleaned_data['id']
        try:
            if(Go.objects.get(pk__iexact=id)):
                raise ValidationError("The id for this Go already exists")
            else:
                return id
        except Go.DoesNotExist:
            return id
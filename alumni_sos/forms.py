from django import forms
from .models import SOSRequest

class SOSRequestForm(forms.ModelForm):
    class Meta:
        model = SOSRequest
        fields = ('title', 'description', 'deadline')
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

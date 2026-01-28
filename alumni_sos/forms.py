from django import forms
from .models import SOSRequest

class SOSRequestForm(forms.ModelForm):
    class Meta:
        model = SOSRequest
        fields = ('title', 'description')

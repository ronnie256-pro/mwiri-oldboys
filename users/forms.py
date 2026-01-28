from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile
from organisation.models import Cohort, House

class RegistrationForm(UserCreationForm):
    cohort = forms.ModelChoiceField(queryset=Cohort.objects.all(), required=False)
    house = forms.ModelChoiceField(queryset=House.objects.all(), required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'cohort', 'house', 'phone_number')

from organisation.models import Profession

class ProfileForm(forms.ModelForm):
    professions = forms.ModelMultipleChoiceField(
        queryset=Profession.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False
    )

    class Meta:
        model = User
        fields = ('professions', 'whatsapp_contact', 'email', 'biography', 'address', 'linkedin_profile', 'website', 'cohort', 'side_hustle')

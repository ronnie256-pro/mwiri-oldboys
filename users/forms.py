from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, SideHustle
from organisation.models import Cohort, House, Profession

class RegistrationForm(UserCreationForm):
    cohort = forms.ModelChoiceField(queryset=Cohort.objects.all(), required=False)
    house = forms.ModelChoiceField(queryset=House.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].help_text = ''

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'first_name', 
            'last_name', 
            'email', 
            'cohort', 
            'house', 
            'phone_number'
        )

class ProfileForm(forms.ModelForm):
    profession = forms.ModelChoiceField(
        queryset=Profession.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )

    class Meta:
        model = User
        # 'address' is the database name, 'Business address' was the label causing the crash
        fields = (
            'profession', 
            'whatsapp_contact', 
            'email', 
            'address', 
            'linkedin_profile', 
            'website', 
            'x_account', 
            'tiktok_account', 
            'youtube_account', 
            'facebook_account'
        )
        
        # This dictionary handles the human-readable names on the frontend
        labels = {
            'address': 'Business Address',
            'whatsapp_contact': 'WhatsApp Number',
            'linkedin_profile': 'LinkedIn URL',
            'x_account': 'X (Twitter)',
            'tiktok_account': 'TikTok',
            'youtube_account': 'YouTube Channel',
            'facebook_account': 'Facebook Page'
        }
        
        # Adding modern styling attributes to the inputs
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'address': forms.TextInput(attrs={'placeholder': 'eg. Kampala, Jinja road, Uganda house, 7th floor, room 07'}),
            'linkedin_profile': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/...'}),
            'website': forms.URLInput(attrs={'placeholder': 'Get a website in 24 hours'}),
            'whatsapp_contact': forms.TextInput(attrs={'placeholder': '+2567XXXXXXXX only not 07xxxxxxxx'}),
            'x_account': forms.URLInput(attrs={'placeholder': 'https://x.com/yourhandle'}),
            'tiktok_account': forms.URLInput(attrs={'placeholder': 'https://tiktok.com/@yourhandle'}),
            'youtube_account': forms.URLInput(attrs={'placeholder': 'https://youtube.com/yourchannel'}),
            'facebook_account': forms.URLInput(attrs={'placeholder': 'https://facebook.com/yourpage'}),
        }

class SideHustleForm(forms.ModelForm):
    class Meta:
        model = SideHustle
        fields = ('title', 'details', 'address', 'image_1', 'image_2')
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Maximum 50 words describing your hustle.'}),
        }
from django import forms
from .models import Candidate, Position

class CandidateApplicationForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['position', 'manifesto']
        widgets = {
            'manifesto': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Share your vision, promises, and reasons why you are the best fit for this position...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter positions to only show those belonging to active election categories
        self.fields['position'].queryset = Position.objects.filter(category__is_active=True)
        # Customize the label to show both position title and category name
        self.fields['position'].label_from_instance = lambda obj: f"{obj.title} ({obj.category.name})"
        self.fields['position'].empty_label = "Select a Position"

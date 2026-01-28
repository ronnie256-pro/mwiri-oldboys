from django import forms
from .models import TeaserQuestion

class TeaserQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for i, question in enumerate(questions):
            self.fields[f'question_{question.id}'] = forms.ModelChoiceField(
                queryset=question.answers.all(),
                widget=forms.RadioSelect,
                label=question.question_text,
                required=True
            )

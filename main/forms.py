from django import forms
from .models import Feedback

from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name',
                'class': 'feedback-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'feedback-input'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Write your feedback here...',
                'class': 'feedback-textarea'
            }),
        }
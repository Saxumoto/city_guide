from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Review

class CustomUserCreationForm(UserCreationForm):
    """Custom form for user registration."""
    email = forms.EmailField(
        required=True,
        label='Email Address',
        help_text='Required. Must be a valid email address.'
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


class ReviewForm(forms.ModelForm):
    """Form for submitting a review and rating."""
    class Meta:
        model = Review
        # We only let the user choose the rating and comment. 
        # The 'attraction' and 'user' fields are set automatically in the view.
        fields = ['rating', 'comment'] 
        
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }
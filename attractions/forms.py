from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Review, Attraction

class CustomUserCreationForm(UserCreationForm):
    """Custom form for user registration."""
    email = forms.EmailField(
        required=True,
        label='Email Address',
        help_text='Required. Must be a valid email address.'
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("A user with this email already exists.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


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
    
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if comment and len(comment.strip()) < 10:
            raise forms.ValidationError("Please provide a more detailed review (at least 10 characters).")
        return comment


class AttractionForm(forms.ModelForm):
    """Custom form for attraction creation/editing with validation."""
    class Meta:
        model = Attraction
        fields = ['name', 'description', 'category', 'location', 'latitude', 'longitude', 'image', 'is_open']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    
    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if latitude is not None:
            if latitude < -90 or latitude > 90:
                raise forms.ValidationError("Latitude must be between -90 and 90 degrees.")
        return latitude
    
    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if longitude is not None:
            if longitude < -180 or longitude > 180:
                raise forms.ValidationError("Longitude must be between -180 and 180 degrees.")
        return longitude
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large (maximum 5MB).")
            # Check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError("Unsupported file format. Please upload a JPG, PNG, GIF, or WEBP image.")
        return image
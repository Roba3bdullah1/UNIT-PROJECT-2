from django import forms 
from .models import Trip
from .models import Comment

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'description', 'location', 'date', 'category', 'image', 'publisher_name']
        widgets = {
            'publisher_name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'comment', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'comment': forms.Textarea(attrs={'class': 'form-control form-control-sm','placeholder': 'Your Comment','rows': 2,}),
            'rating': forms.RadioSelect(attrs={'class': 'd-flex gap-3 fs-3'}),
        }
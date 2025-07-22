from django import forms 
from .models import Trip

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

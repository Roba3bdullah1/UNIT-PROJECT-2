from django import forms 
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title' , 'description' , 'loaction' , 'date' , 'image']
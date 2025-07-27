from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from trip.models import Trip
from trip.forms import TripForm
from main.forms import ContactForm
from django.contrib import messages
from main.forms import ContactForm


def home_view(request:HttpRequest):
    trips = Trip.objects.order_by('-date')[0:3]
    categories = Trip.Category.choices  

    return render(request, 'main/home.html', { 'trips': trips,'categories': categories })



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully. Thank you!")
            return redirect('main:contact_view')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})

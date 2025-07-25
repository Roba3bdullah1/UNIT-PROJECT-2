from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from trip.models import Trip
from trip.forms import TripForm
import trip.views


def home_view(request:HttpRequest):
    trips = Trip.objects.order_by('-date')[0:3]
    categories = Trip.Category.choices

    context = {
        'trips': trips,
        'categories':categories,
    }
    return render(request, 'main/home.html',context)


def contact_view(request:HttpRequest):

    return render(request, 'main/contact.html',)


from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from trip.models import Trip
from trip.forms import TripForm

def home_view(request:HttpRequest):
    trips = Trip.objects.order_by('-date')[0:3]
    return render(request, 'main/home.html', {"trips": trips})


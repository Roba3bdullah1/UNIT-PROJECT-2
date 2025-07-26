from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from trip.models import Trip,InspirationVideo
from trip.forms import TripForm
import trip.views


def home_view(request:HttpRequest):
    trips = Trip.objects.order_by('-date')[0:3]
    categories = Trip.Category.choices  
    inspiration_categories = InspirationVideo.CATEGORY_CHOICES  

    return render(request, 'main/home.html', { 'trips': trips,'categories': categories,'inspiration_categories': inspiration_categories, })


def contact_view(request:HttpRequest):

    return render(request, 'main/contact.html',)


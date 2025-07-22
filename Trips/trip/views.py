from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse

from trip.models import Trip
from .forms import TripForm

# Create your views here.


def all_trips_view(request:HttpRequest):
    trips = Trip.objects.all()
    return render(request, "trip/all_trips.html", {"trips":trips})

def trip_detail_view(request:HttpRequest, trip_id:int):
    trip = Trip.objects.get(pk=trip_id)
    return render(request, 'trips/trip_detail.html', {"trip" : trip})


def add_trip_view(request:HttpRequest):

    form = TripForm()
    if request.method == "POST":
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trip:all_trips_view')
        else:
            print("not valid form", form.errors)

    return render(request, "trip/add_trip.html", {'form' : form})

def update_trip_view(request:HttpRequest,trip_id):
    trip = Trip.objects.get(pk=trip_id)

    if request.method == "POST":
        form = TripForm(instance=trip, data=request.POST, files=request.FILES)
        form.save()
        return redirect("trip_detail_view", trip_id=trip.id)

    return render(request, "trip/trip_update.html", {"trip":trip})

def delete_trip_view(request:HttpRequest, trip_id:int):
    trip = Trip.objects.get(pk=trip_id)
    trip.delete()
    return redirect("main:home_view")


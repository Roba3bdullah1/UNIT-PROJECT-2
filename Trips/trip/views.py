from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse

from .models import Trip,Comment
from .forms import TripForm
from django.contrib import messages

# Create your views here.

from .models import Trip

def all_trips_view(request: HttpRequest):
    trips = Trip.objects.all()

    category = request.GET.get("category")
    if category and category != "all":
        trips = trips.filter(category=category)

    return render(request, "trip/all_trips.html", {"trips": trips,"CategoryChoices": Trip.Category.choices})


def trip_detail_view(request:HttpRequest, trip_id:int):
    trip = Trip.objects.get(pk=trip_id)
    related_trips = Trip.objects.filter(category=trip.category)[0:3]
    comments= Comment.objects.filter(trip=trip)

    return render(request, 'trip/trip_detail.html', {"trip" : trip , 'related_trips': related_trips , 'comments':comments})
                                            
def add_trip_view(request:HttpRequest):

    form = TripForm()
    if request.method == "POST":
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
         form.save()
         messages.success(request, "Trip added successfully!")
         return redirect('trip:all_trips_view')
        else:
            print("not valid form", form.errors)

    return render(request, "trip/add_trip.html", {'form' : form})

def update_trip_view(request: HttpRequest, trip_id):
    trip = Trip.objects.get(pk=trip_id)

    if request.method == "POST":
        form = TripForm(instance=trip, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("trip_detail_view", trip_id=trip.id)
    else:
        form = TripForm(instance=trip)

    return render(request, "trip/update_trip.html", {"form": form, "trip": trip})

def delete_trip_view(request:HttpRequest, trip_id:int):
    trip = Trip.objects.get(pk=trip_id)
    trip.delete()
    return redirect("main:home_view")



def search_trip_view(request: HttpRequest):
    search_input = request.GET.get("search")
    
    if search_input:
        trips = Trip.objects.filter(name__icontains=search_input)
    else:
        trips = Trip.objects.none()
    
    return render(request, 'trip/search_trip.html', {'trips': trips, 'search_input': search_input})


def add_comment_view(request: HttpRequest, trip_id):
    if request.method == "POST":
        trip_object = Trip.objects.get(pk=trip_id)
        new_comment = Comment(
            trip=trip_object,
            name=request.POST["name"],
            comment=request.POST["comment"]
        )
        new_comment.save()

    return redirect("trip:trip_detail_view", trip_id=trip_id)


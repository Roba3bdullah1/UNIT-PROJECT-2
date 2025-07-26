import random
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from .models import Trip,Comment,InspirationVideo
from .forms import TripForm
from django.contrib import messages
from django.db.models import Q
from . import views
from .forms import CommentForm
from .models import Trip

def all_trips_view(request: HttpRequest):
    trips = Trip.objects.all()

    category = request.GET.get("category")
    if category and category != "all":
        trips = trips.filter(category=category)
    
    return render(request, "trip/all_trips.html", {"trips": trips,"CategoryChoices": Trip.Category.choices ,"InspirationVideo":InspirationVideo.CATEGORY_CHOICES})


def trip_detail_view(request:HttpRequest, trip_id:int):
    trip = Trip.objects.get(pk=trip_id)
    related_trips = Trip.objects.filter(category=trip.category)[0:3]
    comments= Comment.objects.filter(trip=trip)
    form = CommentForm()

    return render(request, 'trip/trip_detail.html', {"trip" : trip , 'related_trips': related_trips , 'comments': comments,'form': form})
                                            
def add_trip_view(request: HttpRequest):

    form = TripForm()
    if request.method == "POST":
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save()  

            trip.latitude = request.POST.get("latitude")
            trip.longitude = request.POST.get("longitude")

            trip.save() 
            messages.success(request, "Trip added successfully!")
            return redirect('trip:all_trips_view')
        else:
            print("Form not valid:", form.errors)

    return render(request, "trip/add_trip.html", {'form': form})

def update_trip_view(request: HttpRequest, trip_id):
    trip = Trip.objects.get(pk=trip_id)

   
    if request.method == "POST":
        form = TripForm(instance=trip, data=request.POST, files=request.FILES)
        if form.is_valid():
            updated_trip = form.save(commit=False)
            lat = request.POST.get("latitude")
            lng = request.POST.get("longitude")
            if lat and lng:
                updated_trip.latitude = float(lat)
                updated_trip.longitude = float(lng)
            updated_trip.save()
            messages.success(request, "Trip updated successfully!")
           
            return redirect("trip:trip_detail_view", trip_id=trip.id)
    else:
        form = TripForm(instance=trip)

    return render(request, "trip/update_trip.html", {"form": form, "trip": trip})

def delete_trip_view(request:HttpRequest, trip_id:int):
    trip = Trip.objects.get(pk=trip_id)
    trip.delete()
    return redirect("main:home_view")



def search_trip_view(request: HttpRequest):
    search_input = request.GET.get("search", "")
    category_filter = request.GET.get("category", "")

    trips = Trip.objects.all()
    if search_input:
        trips = trips.filter(
            Q(title__icontains=search_input) | Q(location__icontains=search_input)
        )

    if category_filter:
        trips = trips.filter(category=category_filter)

    if not search_input and not category_filter:
        trips = Trip.objects.none()

    context = {
        "trips": trips,
        "search_input": search_input,
        "category_filter": category_filter,
        "categories": Trip.Category.choices,  
    }

    return render(request, "trip/search_trip.html", context)


def add_comment_view(request: HttpRequest, trip_id):
    if request.method == "POST":
        trip_object = Trip.objects.get(pk=trip_id)
        new_comment = Comment(
            trip=trip_object,
            name=request.POST["name"],
            comment=request.POST["comment"],
            rating=request.POST.get("rating", "😊")  
        )
        new_comment.save()

    return redirect("trip:trip_detail_view", trip_id=trip_id)

def inspiration_view(request):
    selected_category = request.GET.get("category")
    video = None

    if selected_category:
        videos = InspirationVideo.objects.filter(category=selected_category)
        if videos.exists():
            video = random.choice(videos)

    return render(request, "trip/inspiration.html", {"video": video,"categories": InspirationVideo.CATEGORY_CHOICES,"selected_category": selected_category})


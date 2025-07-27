import random
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from .models import Trip,Comment
from .forms import TripForm
from django.contrib import messages
from django.db.models import Q
from . import views
from .forms import CommentForm
from .models import Trip
from django.core.paginator import Paginator
import re



def all_trips_view(request: HttpRequest):
    trips = Trip.objects.all()

    category = request.GET.get("category")
    if category and category != "all":
        trips = trips.filter(category=category)
    
    paginator = Paginator(trips,6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "trip/all_trips.html", {"trips": trips,"CategoryChoices": Trip.Category.choices ,"page":page})


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



def convert_to_embed(url):
   
    youtube_regex = r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/))([^\?&]+)"
    match = re.search(youtube_regex, url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    return None

def inspiration_view(request):
    import random

    selected_category = request.GET.get("category")
    current_video = request.GET.get("current")  

    VIDEO_CATEGORIES = {
        "beach": [
            'https://www.youtube.com/watch?v=JvSv5L0bXiw',
            'https://youtu.be/JvSv5L0bXiw?si=CqA0kP_EGTY4MHLX',
            'https://youtu.be/FuTvGzGaj7o?si=cXBmTk5pplkA1NEk'
        ],
        "mountain": [
            "https://youtu.be/YgL0stuYWLc?si=-T753HMVlzg7ddd1",
            "https://youtu.be/_JSlbVqTBlQ?si=6IP7Dk5taGLbzvi-",
            "https://youtu.be/uOkEle1X7fQ?si=vXhAJrkN33lGDzjG",
        ],
        "city": [
            "https://youtu.be/0MQKLUkAUf8?si=Y318EdWnxT1Y-rbI",
            "https://youtu.be/eHAozTJWnS8?si=F_EzaUV9w7X8qLCI",
            "https://youtu.be/1KjA50-U3ig?si=SZnNMIuNlHmZ-5SB",
        ],
        "nature": [
            "https://youtu.be/1Z5D1Hvm6sM?si=59-BuGQAiNOIPY7l",
            "https://youtu.be/es4x5R-rV9s?si=olb0g4Cfc7NPT6XT",
            "https://youtu.be/SMKPKGW083c?si=ICpg1y4NK8WkKGC2",
        ],
    }

    CATEGORY_CHOICES = {
        "beach": "Beaches",
        "mountain": "Mountains",
        "city": "Cities",
        "nature": "Nature",
    }

    def convert_to_embed(url):
        if "watch?v=" in url:
            return url.replace("watch?v=", "embed/")
        elif "youtu.be" in url:
            video_id = url.split("/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return url

    video_url = None
    if selected_category in VIDEO_CATEGORIES:
        choices = VIDEO_CATEGORIES[selected_category]
        if current_video:
            current_raw = current_video.replace("embed/", "watch?v=")
            choices = [url for url in choices if convert_to_embed(url) != current_video]

        if choices:
            raw_url = random.choice(choices)
            video_url = convert_to_embed(raw_url)

    return render(request, "trip/inspiration.html", {
        "categories": CATEGORY_CHOICES,
        "selected_category": selected_category,
        "video_url": video_url,
    })


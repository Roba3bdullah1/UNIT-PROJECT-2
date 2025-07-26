from django.urls import path
from . import views
from trip.models import Trip

app_name = 'trip'

urlpatterns = [
   path("all/", views.all_trips_view, name='all_trips_view'),
   path("detail/<trip_id>/", views.trip_detail_view, name="trip_detail_view"),
   path('add/', views.add_trip_view, name= 'add_trip_view'),
   path('update/<trip_id>/', views.update_trip_view, name='update_trip_view'),
   path('delete/<trip_id>/',views.delete_trip_view, name='delete_trip_view'),
   path('trips/search/', views.search_trip_view, name='search_trip_view'),
   path('trips/comment/add/<int:trip_id>/', views.add_comment_view, name='add_comment_view'),
   path("inspiration/", views.inspiration_view, name="inspiration_view"),

]
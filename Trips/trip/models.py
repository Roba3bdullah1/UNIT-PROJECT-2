from django.db import models


# Create your models here.

class Trip(models.Model):

    class Category(models.TextChoices):
        ADVENTURE = 'adventure', 'Adventure & Exploration'
        HISTORICAL = 'historical', 'Historical & Cultural'
        BEACH = 'beach', 'Beach & Relaxation'
        MOUNTAIN = 'mountain', 'Mountain & Hiking'
        CAMPING = 'camping', 'Camping & Outdoor'
        CITY = 'city', 'City Tours & Urban'
        NATURE = 'nature', 'Nature & Wildlife'
      
    publisher_name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    latitude = models.FloatField(null = True, blank = True)
    longitude = models.FloatField(null = True, blank = True)
    date = models.DateField()
    category = models.CharField(max_length=50,choices=Category.choices,default=Category.CITY)
    image = models.ImageField(upload_to="images/", default="images/default.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    



class Comment(models.Model):
    

    class RatingChoices(models.IntegerChoices):
        RATE1= 1, "😡 Terrible Trip"
        RATE2= 2, "😐 Not Great"
        RATE3= 3, "😊 Nice Trip"
        RATE4= 4, "😍 Amazing Experience"
 

    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    comment = models.TextField()
    rating = models.SmallIntegerField(choices=RatingChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)



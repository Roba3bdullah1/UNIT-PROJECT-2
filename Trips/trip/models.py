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
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.CITY)
    image = models.ImageField(upload_to="images/", default="images/default.jpg")

   


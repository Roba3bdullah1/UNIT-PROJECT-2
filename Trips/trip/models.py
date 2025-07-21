from django.db import models

# Create your models here.

class Trip(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    loaction = models.CharField(max_length=200)
    latitude = models.FloatField(null = True, blank = True)
    longitude = models.FloatField(null = True, blank = True)
    date = models.DateField()
    image = models.ImageField(upload_to="images/", default="images/default.jpg")




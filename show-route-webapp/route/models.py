from django.contrib.gis.db import models

# Create your models here.

class Attraction(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    location = models.PointField()

from django.contrib.gis.db import models

# Create your models here.


class Attraction(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, null=True)
    location = models.PointField()

    def __str__(self):
        s = self.name
        if self.country:
            s += ', ' + self.country
        if self.city:
            s += ', ' + self.city
        return s


class Sight(models.Model):
    # id          integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    # rating      float,
    # name        text NOT NULL,
    # description text,
    # city_id     integer REFERENCES city (id),
    # country_id  integer REFERENCES country (id),
    # UNIQUE (name, city_id)
    name = models.TextField(null=False)
    description = models.TextField()
    rating = models.FloatField()
    longitude = models.FloatField()
    latitude = models.FloatField()

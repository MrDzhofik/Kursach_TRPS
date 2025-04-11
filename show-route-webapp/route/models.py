from django.contrib.gis.db import models

# Create your models here.


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

    class Meta:
        db_table = 'sight'
        managed = False

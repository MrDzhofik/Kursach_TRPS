from django.core.management.base import BaseCommand
import json
from route.models import Attraction
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('route/management/commands/export_hotels.geojson', 'rb') as f:
            data = json.load(f)
            
            for elem in data['features']:
                attraction = Attraction()
                i = elem['properties']
                coord = elem['geometry']
                if 'name' in i:
                    attraction.name = i['name']
                else: 
                    continue
                if 'addr:city' in i:
                    attraction.city = i['addr:city']
                if 'addr:country' in i:
                    attraction.country = i['addr:country']
                if 'addr:housenumber' in i and 'addr:street' in i:
                    attraction.address = i['addr:street'] + " " + i['addr:housenumber']
                if not isinstance(coord['coordinates'][0], float):
                    long, lat = coord['coordinates'][0][0]
                    attraction.location = Point(long, lat)
                    

                    attraction.save()
                
        print('finished')
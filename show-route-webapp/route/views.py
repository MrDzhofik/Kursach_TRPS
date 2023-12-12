import folium
from django.shortcuts import render,redirect
from . import getroute, forms
from .models import Attraction
from django.contrib.gis.geos import GEOSGeometry
import requests
import polyline

def showmap(request):
    form = forms.SimpleForm()
    return render(request,'showmap.html', context={'form':form})

def get_route(points):
    url = "http://router.project-osrm.org/route/v1/driving/"
    for i in points:
        long, lat = map(float, i)
        url += f"{lat},{long};"
    url = url[:-1]
    print(url)
    r = requests.get(url) 
    if r.status_code != 200:
        return {}
    res = r.json()   
    routes = polyline.decode(res['routes'][0]['geometry'])
    point = res['waypoints']
    waypoints = ''
    start_point = [point[0]['location'][1], point[0]['location'][0]]
    for i in range(1, len(point) - 1):
        waypoints += str(point[i]['location'][1]) + " " + str(point[i]['location'][0]) + '!'
    end_point = [point[-1]['location'][1], point[-1]['location'][0]]
    distance = res['routes'][0]['distance']
    
    out = {'route':routes,
           'start_point':start_point,
           'waypoints': waypoints,
           'end_point':end_point,
           'distance':distance
          }

    return out

def showroute(request):
    data = request.POST
    figure = folium.Figure()
    points = []
    for key in data.keys():
        if key != 'csrfmiddlewaretoken':
            i = data.get(key)
            geo = Attraction.objects.get(id=i)
            long = geo.location
            long = GEOSGeometry(long)
            lat = long.y
            long = long.x
            points.append([lat, long])

    route=get_route(points)
    m = folium.Map(location=[(route['start_point'][0]),
                                 (route['start_point'][1])], 
                       zoom_start=10)
    m.add_to(figure)
    folium.PolyLine(route['route'],weight=8,color='blue',opacity=0.6).add_to(m)
    coords = route['waypoints'].split('!')
    print('coords:', coords)
    for key in range(len(coords)):
        l = coords[key].split()
        if l:
            print(l)
            coord = tuple(map(float, (l[0], l[1])))
            folium.Marker(location=coord,icon=folium.Icon(icon='pause', color='blue')).add_to(m)
    folium.Marker(location=route['start_point'],icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()
    context={'map':figure._repr_html_()}
    return render(request,'showroute.html',context)

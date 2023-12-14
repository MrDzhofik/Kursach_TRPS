import folium
from django.shortcuts import render
from . import getroute, forms
from .models import Attraction
from django.contrib.gis.geos import GEOSGeometry

def showmap(request):
    form = forms.SimpleForm()
    return render(request,'showmap.html', context={'form':form})

def showroute(request):
    data = request.POST
    figure = makeroute(data)
    context={'map':figure._repr_html_()}
    return render(request,'showroute.html',context)

def makeroute(data):
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

    route=getroute.get_route(points)
    m = folium.Map(location=[(route['start_point'][0]),
                                 (route['start_point'][1])], 
                       zoom_start=10)
    m.add_to(figure)
    folium.PolyLine(route['route'],weight=8,color='blue',opacity=0.6).add_to(m)
    coords = route['waypoints'].split('!')
    for key in range(len(coords)):
        l = coords[key].split()
        if l:
            print(l)
            coord = tuple(map(float, (l[0], l[1])))
            folium.Marker(location=coord,icon=folium.Icon(icon='pause', color='blue')).add_to(m)
    folium.Marker(location=route['start_point'],icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()

    return figure
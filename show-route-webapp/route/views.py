import folium
from django.shortcuts import render
from . import getroute, forms
from .models import Attraction
from django.contrib.gis.geos import GEOSGeometry
from geopy.distance import geodesic

def showmap(request):
    form = forms.SimpleForm()
    return render(request,'showmap.html', context={'form':form})

def showroute(request):
    data = request.POST
    figure = makeroute(data)
    context={'map':figure._repr_html_()}
    return render(request,'showroute.html',context)

# Поиск минимального элемента в массиве
def min(row, indexes):
    min_dist = float("inf")
    index = 0
    for j in range(len(row)):
        if row[j] < min_dist and row[j] != 0 and j not in indexes:
            index = j
            min_dist = row[j]
    
    return index

# Расчет расстояния геогрфических точек
def calc_distance(points):
    distance = []
    dist = []
    for i in range(len(points)):
        for j in range(len(points)):
            if j == i:
                dist.append(0)
            else:
                dist.append(round(geodesic(points[i], points[j]).km, 2))
        distance.append(dist)
        dist = []

    return distance



def makeroute(data):
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

    # Если количество точек больше 4, то делаем оптимизацию методом ближайшего соседа
    if (len(points) >= 4):
        points = nearest_neighbour(points)


    route=getroute.get_route(points)
    figure = create_map(route)

    return figure

# Создание карты и маркеров
def create_map(route):
    figure = folium.Figure()
    m = folium.Map(location=[(route['start_point'][0]), (route['start_point'][1])], zoom_start=10)
    m.add_to(figure)
    folium.PolyLine(route['route'],weight=8,color='blue',opacity=0.6).add_to(m)
    coords = route['waypoints'].split('!')
    for key in range(len(coords)):
        l = coords[key].split()
        if l:
            coord = tuple(map(float, (l[0], l[1])))
            folium.Marker(location=coord,icon=folium.Icon(icon='pause', color='blue')).add_to(m)
    folium.Marker(location=route['start_point'],icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()

    return figure


def nearest_neighbour(points):
    indexes = [0]
    matrix = calc_distance(points)
    new_points = []
    index = 0
    for i in range(1, len(points) - 1):
        ok = min(matrix[index], indexes)
        indexes.append(ok)
        index = ok
    indexes.append(len(points) - 1)
    for i in range(len(indexes)):
        new_points.append(points[indexes[i]])
    
    return new_points
    
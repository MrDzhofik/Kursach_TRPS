import folium
from django.shortcuts import render,redirect
from . import getroute, forms
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
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][-1]['location'][1], res['waypoints'][-1]['location'][0]]
    distance = res['routes'][0]['distance']
    
    out = {'route':routes,
           'start_point':start_point,
           'end_point':end_point,
           'distance':distance
          }

    return out

def showroute(request):
    data = request.POST
    print(data)
    figure = folium.Figure()
    points = []
    for key, value in data.items():
        if key != 'csrfmiddlewaretoken':
            value = value.split()
            points.append(value)

    route=get_route(points)
    m = folium.Map(location=[(route['start_point'][0]),
                                 (route['start_point'][1])], 
                       zoom_start=10)
    m.add_to(figure)
    folium.PolyLine(route['route'],weight=8,color='blue',opacity=0.6).add_to(m)
    folium.Marker(location=route['start_point'],icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()
    context={'map':figure._repr_html_()}
    return render(request,'showroute.html',context)

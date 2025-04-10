import requests
import polyline

from .distance import nearest_neighbour
from .models import Sight
from .map import create_map


def get_route(points):
    url = "http://router.project-osrm.org/route/v1/driving/"
    print(points)
    for i in points:
        long, lat = map(float, i)
        url += f"{lat},{long};"
    url = url[:-1]
    r = requests.get(url, timeout=100)
    if r.status_code != 200:
        return {}
    res = r.json()
    routes = polyline.decode(res['routes'][0]['geometry'])
    point = res['waypoints']
    waypoints = ''
    start_point = [point[0]['location'][1], point[0]['location'][0]]
    for i in range(1, len(point) - 1):
        waypoints += str(point[i]['location'][1]) + " "
        waypoints += str(point[i]['location'][0]) + '!'
    end_point = [point[-1]['location'][1], point[-1]['location'][0]]
    distance = res['routes'][0]['distance']

    out = {'route': routes,
           'start_point': start_point,
           'waypoints': waypoints,
           'end_point': end_point,
           'distance': distance}

    return out


def makeroute(data):
    points = []
    for key in data.keys():
        if key != 'csrfmiddlewaretoken':
            i = data.get(key)

            geo = Sight.objects.get(id=i)
            longitude = geo.longitude
            latitude = geo.latitude
            points.append([longitude, latitude])

    # Если количество точек больше 4, то делаем оптимизацию
    # методом ближайшего соседа
    if len(points) >= 4:
        points = nearest_neighbour(points)

    route = get_route(points)
    figure = create_map(route)

    return figure

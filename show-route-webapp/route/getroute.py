import requests
import polyline

def get_route(points):
    url = "http://router.project-osrm.org/route/v1/driving/"
    for i in points:
        long, lat = map(float, i)
        url += f"{lat},{long};"
    url = url[:-1]
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
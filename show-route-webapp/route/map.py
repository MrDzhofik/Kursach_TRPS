import folium


# Создание карты и маркеров
def create_map(route):
    figure = folium.Figure()
    m = folium.Map(location=[(route['start_point'][0]),
                             (route['start_point'][1])], zoom_start=10)
    m.add_to(figure)
    folium.PolyLine(route['route'], weight=8,
                    color='blue', opacity=0.6).add_to(m)
    coords = route['waypoints'].split('!')
    for key in range(len(coords)):
        point = coords[key].split()
        if point:
            coord = tuple(map(float, (point[0], point[1])))
            folium.Marker(
                location=coord,
                icon=folium.Icon(
                    icon='pause',
                    color='blue'
                )).add_to(m)
    folium.Marker(
        location=route['start_point'],
        icon=folium.Icon(
            icon='play',
            color='green'
        )).add_to(m)
    folium.Marker(
        location=route['end_point'],
        icon=folium.Icon(
            icon='stop',
            color='red'
        )).add_to(m)
    figure.render()

    return figure

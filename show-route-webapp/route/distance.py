from geopy.distance import geodesic


def min_dist(row: list, indexes):
    """ Поиск минимального элемента в массиве (индекс) """
    min_distance = float("inf")
    index = 0
    for j in range(len(row)):
        if row[j] < min_distance and row[j] != 0 and j not in indexes:
            index = j
            min_distance = row[j]

    return index


# Расчет расстояния геогрaфических точек
def calc_distance(points):
    coord = []
    for point in points:
        coord.append((point[1], point[2]))
    distance = []
    dist = []
    for i in range(len(points)):
        for j in range(len(points)):
            if j == i:
                dist.append(100000000)
            else:
                dist.append(round(geodesic(coord[i], coord[j]).km, 2))
        distance.append(dist)
        dist = []

    return distance


def nearest_neighbour(points: list):
    indexes = [0]
    matrix = calc_distance(points)
    new_points = []
    index = 0
    for i in range(len(points) - 1):
        ok = min_dist(matrix[index], indexes)
        indexes.append(ok)
        index = ok
    for i in range(len(indexes)):
        new_points.append(points[indexes[i]])

    return new_points

import math


def num2deg(x, y, zoom):
    n = 2.0 ** zoom
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return (lon_deg, lat_deg)

def getTileCoordinates(x, y, zoom):
    coords = list(num2deg(x, y, zoom)) + list(num2deg(x + 1 % 2**zoom, y + 1 % 2**zoom, zoom))
    return coords


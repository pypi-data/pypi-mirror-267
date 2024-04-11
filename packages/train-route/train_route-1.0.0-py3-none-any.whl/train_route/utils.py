import math
import pyproj

geod = pyproj.Geod(ellps='WGS84')

def plane_distance(lats, lons):
    x0, x1 = lats
    y0, y1 = lons
    return math.sqrt((x1 - x0)**2 + (y1 - y0)**2)

def spherical_distance(lats, lons):
    return geod.line_lengths(lons, lats)[0]

def spherical_rotation(lats, lons):
    x0, x1 = lats
    y0, y1 = lons
    fwd_azimuth, back_azimuth, distance = geod.inv(y0, x0, y1, x1)
    return fwd_azimuth

def cumulative_distance(latitudes, longitudes, *, distance=plane_distance):
    distances = [0.]
    for i in range(1, len(latitudes)):
        lats = latitudes[i - 1:i + 1]
        lons = longitudes[i - 1:i + 1]
        local_distance = distance(lats, lons)
        distances.append(local_distance)
    return cumsum(distances)

def interpolate(xs, index, delta):
    x0 = xs[index - 1]
    x1 = xs[index]
    return x0 + delta * (x1 - x0)

def cumsum(xs:list):
    cs = list(xs)
    for i in range(1, len(cs)):
        cs[i] += cs[i - 1]
    return cs

def state(start, end):
    lat0, lon0 = start
    lat1, lon1 = end
    return [
        (lat0 + lat1) / 2,
        (lon0 + lon1) / 2,
        spherical_rotation((lat0, lat1), (lon0, lon1))
    ]

def is_inside(position, window):
    lat, lon = position
    d = window['distance']([window['center']['lat'], lat], [window['center']['lon'], lon])

    if d <= window['radius']:
        return True
    else:
        return False
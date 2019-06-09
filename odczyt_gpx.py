# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:11:57 2019

@author: lenovo
"""

import gpxpy
from math import sin, cos, sqrt, pi

# Funkcja pobierajaca dne z pliku gpx
def importGpx(filename):
    lat = []
    lon = []
    ele = []
    dates = []
    
    # Wczytanie pliku
    with open(filename, "r") as f: 
        gpx = gpxpy.parse(f)
    
    # Wczytanie kolejnych wartosci do odpowiednich list
    for track in gpx.tracks:
        for seg in track.segments:
            for point in seg.points:
                lon.append(point.longitude)
                lat.append(point.latitude)
                ele.append(point.elevation)
                dates.append(point.time)
    return lat, lon, ele, dates

# Przeliczenie koordynatow na XYZ
def coordToXyz(lon, lat, alt):
    lat = lat/180*pi
    lon = lon/180*pi
    alt = alt + 6378137
    x = alt * cos(lat) * sin(lon)
    y = alt * sin(lat)
    z = alt * cos(lat) * cos(lon)
    return x, y, z

# Policzenie dystansu przy pomocy XYZ
def distXyz(x1, y1, z1, x2, y2, z2):
    dx = x1 - x2
    dy = y1 - y2
    dz = z1 - z2
    dist = sqrt(dx*dx + dy*dy + dz*dz)
    return dist

# Policzenie dystansu przy pomocy koordynatow
def distance(lon1, lat1, alt1, lon2, lat2, alt2):
    x1, y1, z1 = coordToXyz(lon1, lat1, alt1)
    x2, y2, z2 = coordToXyz(lon2, lat2, alt2)
    dist = distXyz(x1, y1, z1, x2, y2, z2)
    return dist



    
    
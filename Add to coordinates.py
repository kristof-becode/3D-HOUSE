import os
import numpy as np
import descartes
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("white")
import geopandas as gpd
import rasterio as rio
import earthpy as et
import earthpy.plot as ep
import geopy
from geopy.geocoders import Nominatim # I need to explicitly import Nominatim as such
import folium

locator = Nominatim(user_agent="myGeocode")
location = locator.geocode('35, Snoekstraat, Ghent, Belgium')
print('Latitude = {}, Longitude = {}'.format(location.latitude, location.longitude))

map1 = folium.Map(
    location=[location.latitude,location.longitude],
    tiles='cartodbpositron',
    zoom_start=12)
#df.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]]).add_to(map1), axis=1)
#map1
folium.Marker(
    location=[location.latitude, location.longitude],
    popup='location',
    icon=folium.Icon(icon='info-sign')
).add_to(map1)
map1.save('/home/becode/data/kaart.html')
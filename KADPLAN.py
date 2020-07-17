import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("white")
import pandas as pd
import geopandas as gpd
import rasterio as rio
import earthpy as et
import earthpy.plot as ep
import geopy
from geopy.geocoders import Nominatim # I need to explicitly import Nominatim as such
#import folium
from pyproj import Proj, transform
import plotly.graph_objects as go
pd.set_option('display.width',400)
pd.set_option('display.max_columns', 40)

"""

plot_loc = gpd.read_file('/home/becode/KadPlan/Bpn_CaPa.shp')
print(plot_loc.head(10))
#plot_loc.plot()
#plt.show()

dbf_data = gpd.read_file('/home/becode/KadPlan/Bpn_CaPa.dbf') #plotting this gives same as plotting shape .shp and plotting dataframe is also exactly the same
print(dbf_data.head(10))
dbf_data.plot()
plt.show()
"""
# POLYGONEN UIT MYMINFIN SITE
#71382D0700/00G000 ik zie 3 polygonen
# Diestersesteenweg 26
dbf_data = gpd.read_file('/home/becode/KadPlan/Bpn_CaPa.dbf')
print(dbf_data.geometry[dbf_data.CaPaKey == '71382D0700/00G000'])
#euro12.Team.str[0] == 'G'

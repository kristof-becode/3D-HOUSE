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
#import folium
from pyproj import Proj, transform

# retrieve coordinates frm address
locator = Nominatim(user_agent="myGeocode")
location = locator.geocode('36, Maarschalk Fochstraat, Leopoldsburg, Belgium')
print('Latitude = {}, Longitude = {}'.format(location.latitude, location.longitude))

# convert above coordinates to Lambert coordinates
inProj = Proj('epsg:4326')
outProj = Proj('epsg:31370')
la1, lo1 = location.latitude, location.longitude
la2, lo2 = transform(inProj,outProj,la1,lo1)
print(la2,lo2)
# CHM = DSM- DTM

with rio.open('/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif') as plot_dsm:
   dsm = plot_dsm.read(1, masked = True)

#with rio.open('/home/becode/Documents/DTM k25/GeoTIFF/DHMVIIDTMRAS1m_k25.tif') as plot_dtm:
    #dtm = plot_dtm.read(1, masked =True)

#chm = dsm -dtm
"""
plot_dsm.close()
plot_dtm.close()

with rio.open('/home/becode/Documents/DSM k25/GeoTIFF/CHM_k25.tif') as ff:
    ff.write(chm[0],1)


"""

row, col = plot_dsm.index(la2, lo2)
row1, col1 = row- 500, col- 500
row2, col2 = row+ 500, col+ 500
mat = dsm[row1:row2, col1:col2]
print(mat)
ep.plot_bands(mat, title="CHM", cmap="viridis")

plt.show()
"""
#print(rio.transform.index(dsm,la2,lo2))

# create box around coordinates
x,y = (chm.xy((chm.height // 2) - 100, (chm.width // 2) - 100))
row1, col1 = chm.index(x, y)
print(row1, col1)
x,y = (chm.xy((chm.height // 2) + 100, (chm.width // 2) + 100))
row2, col2 = chm.index(x, y)
print(row2, col2)
r = [row1,row2]
c = [col1,col2]
#mat = tiff_plot[np.ix_(r, c)]
mat = chm[row1:row2, col1:col2]

ep.plot_bands(mat, title="CHM", cmap="viridis")

plt.show()
#print(tiff_plot_dtm.res)
#print(tiff_plot_dtm.count)
#print(tiff_plot_dtm.indexes)
"""
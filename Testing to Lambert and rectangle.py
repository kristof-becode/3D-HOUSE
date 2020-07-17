import os
import numpy as np
import descartes
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("white")
import geopandas as gpd
import rasterio as rio
from rasterio import Affine as A
from rasterio.warp import calculate_default_transform, reproject, Resampling
import earthpy as et
import earthpy.plot as ep
from pyproj import Proj, transform

with rio.open('/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif') as tiff_plot_dtm:
    tiff_plot = tiff_plot_dtm.read(1)
print(tiff_plot)
print(tiff_plot_dtm.meta)
print(tiff_plot_dtm.count)
print(tiff_plot_dtm.bounds)
print(tiff_plot_dtm.width)
print(tiff_plot.shape)
print(tiff_plot_dtm.height)
print(tiff_plot_dtm.xy(tiff_plot_dtm.height // 2, tiff_plot_dtm.width // 2)) #another thing he flips ?
print(tiff_plot_dtm.transform)
print("spatial pos upper left: ", tiff_plot_dtm.transform * (0, 0))
print("spatial pos bottom right: ",tiff_plot_dtm.transform * (tiff_plot_dtm.width, tiff_plot_dtm.height))
x, y = (tiff_plot_dtm.bounds.left + 100000, tiff_plot_dtm.bounds.top - 50000)
row, col = tiff_plot_dtm.index(x, y)
print(row, col)
#band1 = tiff_plot_dtm.read(1)
#print(band1[row, col])
###########TRy To crop a piece aroudnt the center of the array:
inProj = Proj('epsg:4326')
outProj = Proj('epsg:31370')
la1, lo1 = 51.04793, 5.21862
la2, lo2 = transform(inProj,outProj,la1,lo1)
print(la2,lo2)
#a,b= la2, lo2
"""
a,b = (tiff_plot_dtm.xy(tiff_plot_dtm.height // 2, tiff_plot_dtm.width // 2))
row, col = tiff_plot_dtm.index(a, b)
print(row, col)
####Create 2 corners of a rectangle
x,y = (tiff_plot_dtm.xy((tiff_plot_dtm.height // 2) - 100, (tiff_plot_dtm.width // 2) - 100))
row1, col1 = tiff_plot_dtm.index(x, y)
print(row1, col1)
x,y = (tiff_plot_dtm.xy((tiff_plot_dtm.height // 2) + 100, (tiff_plot_dtm.width // 2) + 100))
row2, col2 = tiff_plot_dtm.index(x, y)
print(row2, col2)
r = [row1,row2]
c = [col1,col2]
#mat = tiff_plot[np.ix_(r, c)]
mat = tiff_plot[row1:row2, col1:col2]
print(mat)
ep.plot_bands(mat, title="Lidar Digital) Elevation Model (DEM) \n Boulder Flood 2013", cmap="Greys")

plt.show()
"""
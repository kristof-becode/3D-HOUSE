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

#plot_loc = gpd.read_file('/home/becode/Documents/DTM k25/DHMVII_vdc_k25.shp')
#print(plot_loc.head(5))
#plot_loc.plot()

#print(plot_loc.crs) # extent of info in df
#print(plot_loc.total_bounds) # geospatial bounds of data
"""
plot_loc = gpd.read_file('/home/becode/Documents/DTM k25/DHMVII_vdc_k25.shp')

plot_loc.plot()

plot_loc = gpd.read_file('/home/becode/Documents/DSM k25/DHMVII_vdc_k25.shx')
print(plot_loc.head(5))
print(plot_loc.columns)
print(plot_loc['OpnDatum1'].head(5))

print(plot_loc['geometry'].head(10))
read_dbf = gpd.read_file('/home/becode/Documents/DSM k25/DHMVII_vdc_k25.dbf')
print(read_dbf.head(10))
print(read_dbf.columns)
print(read_dbf['geometry'].head(10))
#plot_loc.plot(figsize=(10,10))
#ep.plot(plot_loc)
#plt.show()
##rasterio
lidar_dem_path = '/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif'
with rio.open(lidar_dem_path) as lidar_dem:
    lidar_dem.bounds
    print(lidar_dem.tags(ns='IMAGE_STRUCTURE'))
    lidar_dem_mask = lidar_dem.dataset_mask()
print(lidar_dem_mask)
print(lidar_dem.meta)
print(lidar_dem.res)


#da = xr.open_rasterio('/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif')
#transform = Affine.from_gdal(*da.attrs[’transform’]) # this is important to retain the geographic attributes from the file

lidar_dem_path = '/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif'
with rio.open(lidar_dem_path) as lidar_dem:
    lidar_dem.bounds


#tiff_plot_dsm = rio.open('/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif')
#plt.imshow(tiff_plot_dsm.read(1), cmap='pink')
#plt.show()

tiff_plot_dtm = rio.open('/home/becode/Documents/DTM k25/GeoTIFF/DHMVIIDTMRAS1m_k25.tif')
plt.imshow(tiff_plot_dtm.read(1), cmap='pink')
plt.show()

tiff_plot_dsm = rio.open('/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif')
plt.imshow(tiff_plot_dsm.read(1), cmap='pink')
plt.show()
############
#with rio.open('/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif') as dem_src:
#with rio.open('/home/becode/Documents/DTM k25/GeoTIFF/DHMVIIDTMRAS1m_k25.tif') as dem_src:
with rio.open('/home/becode/Documents/DTM k25/GeoTIFF/DHMVIIDTMRAS1m_k25.tif') as src:
    #paste om te spelen met width enzo
    src_transform = src.transform

    # Zoom out by a factor of 2 from the center of the source
    # dataset. The destination transform is the product of the
    # source transform, a translation down and to the right, and
    # a scaling.
    dst_transform = src_transform*A.translation(
        -src.width/2.0, -src.height/2.0)*A.scale(2.0)

    data = src.read()

    kwargs = src.meta
    kwargs['transform'] = dst_transform

    #dem_src.bounds
    #HIERONDER IS NODIG
    #dtm_pre_arr = dem_src.read(1)

    #print(dtm_pre_arr.tags(ns='IMAGE_STRUCTURE'))
    #dtm_pre_arr_mask = dtm_pre_arr.dataset_mask()

#print(dtm_pre_arr_mask)
#print(dtm_pre_arr.mask)
#print(dtm_pre_arr.res)
#print(dtm_pre_arr)
ep.plot_bands(data,
              title="Lidar Digital Elevation Model (DEM) \n Boulder Flood 2013",
              cmap="Greys")

plt.show()
"""
#tiff_plot_dtm = rio.open('/home/becode/Documents/DTM k25/GeoTIFF/DHMVIIDTMRAS1m_k25.tif')
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
#a,b= la2, lo2
a,b = (tiff_plot_dtm.xy(tiff_plot_dtm.height // 2, tiff_plot_dtm.width // 2))
row, col = tiff_plot_dtm.index(a, b)
print(row, col)
####Create 2 corners of a recatngele
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

#############
"""
#regcoord = rasterio.warp.calculate_default_transform(CRS({‘init’: ‘EPSG:31370’}),CRS({‘init’: ‘EPSG:4326’}),20000, 32000)#EPSG:31370
newBo = rio.warp.transform_bounds(31370, 4326, 194000.0, 178000.0, 226000.0, 198000.0)# densify_pts=21) #omdraaien nodig!!!!!! #left, bottom, right, top – Outermost coordinates in target coordinate reference system.
print(newBo)
#50 smthn = breedtegraad
# 4 smthn = lengtregraad
# dus bounds uit bovenstaande geven koppels breedt/lengte
#Output is left,bottom,right,top => left, top AND right,bottom

####REPROJECT
dst_crs = 'EPSG:4326'

with rio.open('/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif') as src:
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    with rio.open('/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25_reproj.tif', 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rio.band(src, i),
                destination=rio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest)


##
"""

#rasterio.warp.reproject(source, destination=None, src_transform=None, gcps=None, src_crs=None, src_nodata=None, dst_transform=None, dst_crs=None, dst_nodata=None, dst_resolution=None, src_alpha=0, dst_alpha=0, resampling=<Resampling.nearest: 0>, num_threads=1, init_dest_nodata=True, warp_mem_limit=0, **kwargs)
#newSet = rio.warp.reproject(tiff_plot, destination=None, src_crs=31370, dst_crs=4326)
#print(tiff_plot_dtm)
#ep.plot_bands(tiff_plot[2000:4000], title="Lidar Digital) Elevation Model (DEM) \n Boulder Flood 2013", cmap="Greys")

#plt.show()
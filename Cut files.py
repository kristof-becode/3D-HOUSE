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
import plotly.graph_objects as go
"""
cpt=0
for x in range(1, 2):
    print(f"Getting map n°{x}, total tiles : {cpt}")
    #in_path = "/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif" #+tile+"/GeoTIFF/"
    #input_filename = "DHMVIIDSMRAS1m_k"+tile+".tif"

    out_path = "/home/becode/Documents/"
    output_filename = "tile_"

    tile_size_x = 1000
    tile_size_y = 500

    #ds = rio.open('/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif')
    with rio.open('/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif') as plot_dsm:
        dsm = plot_dsm.read (1)

    # ds = gdal.Open(in_path + input_filename)
    #band = ds.GetRasterBand(1)
    #xsize = band.XSize
    #ysize = band.YSize
    for i in range(0, plot_dsm.width, tile_size_x):
        for j in range(0, plot_dsm.height, tile_size_y):
            cpt+=1

            #com_string = str(i)+", "+str(j)+", "+str(tile_size_x)+", "+str(tile_size_y)+" "+"/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25 "+str(out_path)+str(output_filename)+str(cpt)+".tif"
            #com_string = "gdal_translate -of GTIFF -srcwin " +str(i)+", "+str(j)+", "+str(tile_size_x)+", "+str(tile_size_y)+" "+str(in_path)+str(input_filename)+" "+str(out_path)+str(output_filename)+str(cpt)+".tif"
            #os.system(com_string)
            with rio.Env():
                # Write an array as a raster band to a new 8-bit file. For
                # the new file's profile, we start with the profile of the source
                profile = plot_dsm.profile

                # And then change the band count to 1, set the
                # dtype to uint8, and specify LZW compression.
                profile.update(
                    dtype=rio.uint8,
                    count=1,
                    compress='lzw')
                path = os.path.abspath('/home/becode/Documents')
                folder_path = path
                final_path = os.path.join(folder_path, str(i)+ str(j)+ " "+str(tile_size_x)+" "+str(tile_size_y)+" "+str(output_filename)+str(cpt)+".tif")
                with rio.open(final_path, 'w', **profile) as dst:
                    #dst.write([0],1)
                    dst.write(array.astype(rio.uint8), 1)
"""
#plot_tile = rio.open('/home/becode/Documents/tile_dsm25__0.tif')
plot_tile = rio.open("/home/becode/Documents/Tile_dsm25/tile_dsm25__456.tif") #345
tile = plot_tile.read(1)
print(tile)
print(plot_tile.res)
print(plot_tile.meta)
print(plot_tile.count)
print(plot_tile.bounds)
print(plot_tile.width)
print(plot_tile.shape)
print(plot_tile.height)

ep.hist(tile, bins=100)
#ep.plot_bands(tile, title="CHM", cmap="viridis")
plt.show()
plot_tile = rio.open("/home/becode/Documents/Tile_dsm25/tile_dsm25__457.tif") #345
tile = plot_tile.read(1)
print(tile)
print(plot_tile.res)
print(plot_tile.meta)
print(plot_tile.count)
print(plot_tile.bounds)
print(plot_tile.width)
print(plot_tile.shape)
print(plot_tile.height)
ep.hist(tile, bins=100)
#ep.plot_bands(tile, title="CHM", cmap="viridis")
#plt.show()

fig = go.Figure(data=[
    go.Surface(z=tile)

])

fig.show()


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

for i in range(135,136):

    path_in_dsm = "/home/becode/Documents/Tile_dsm25/tile_dsm25__" + str(i) + ".tif"

    with rio.open(path_in_dsm) as plot_dsm :
        dsm = plot_dsm.read(1, masked = True)
        dsm.meta = plot_dsm.profile


    path_in_dtm = "/home/becode/Documents/Tile_dtm25/tile_dtm25__" + str(i) + ".tif"

    with rio.open(path_in_dtm) as plot_dtm:
        dtm = plot_dtm.read(1, masked =True)

    chm = dsm -dtm

    plot_dsm.close()
    plot_dtm.close()

    path_out_chm = "/home/becode/Documents/Tile_chm25/tile_chm25__" + str(i) + ".tif"
    #with rio.open(path_out_chm, "w", **metadata) as dest:
        #dest.write(img)
    with rio.open(path_out_chm, "w", **dsm.meta) as ff:
        ff.write(chm, 1)
    ff.close()



import os.path
import re
import numpy as np
import descartes
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("white")
import geopandas as gpd
import rasterio as rio
import earthpy as et
import earthpy.plot as ep

path = os.path.abspath('/media/becode/EXT/DSMsplit')
folder_path = path
list = ['k1', 'k2','k3','k4','k5','k6','k7','k8','k9','k10','k11','k12','k13','k14','k15','k16','k17',
                    'k18','k19','k20','k21','k22','k23']
# walk trough folder with split DSMs, open them, then open corresponding DTM and subtract both of them to create a CHM, lastly write CHM to file
for path, dirs, files in os.walk(folder_path):
    for file in files:
        if re.match("(.)+.tif", file) is not None: #and all([x in file for x in list]) == False:

            with rio.open(os.path.join(path, file)) as plot_dsm:
                dsm = plot_dsm.read(1, masked=True)
                dsm.meta = plot_dsm.profile

            # change path to read in DTM based upon path DTM
            path_in_dsm = os.path.join(path, file)
            path_in_dtm = path_in_dsm.replace('DSMsplit', 'DTMsplit')
            path_in_dtm = path_in_dtm.replace('dsm', 'dtm')
            with rio.open(path_in_dtm) as plot_dtm:
                    dtm = plot_dtm.read(1, masked=True)
            # subtract terrain model from surface model to create CHM or Canopy Height Model
            chm = dsm - dtm
            # close files
            plot_dsm.close()
            plot_dtm.close()
            # write CHM to file, adjust path from DSM
            path_out_chm = '/media/becode/EXT/CHMsplit/' + file.replace('dsm','chm')
            with rio.open(path_out_chm, "w", **dsm.meta) as ff:
                ff.write(chm, 1)
            ff.close()
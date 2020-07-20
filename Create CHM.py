"""This .py code creates a Canopy Height Model by subtracting the Digital Terrain Model from the Digital Surface Model
    or : CHM = DSM-DTM. This should give us the height of buildings. Masking DSM files with a polygon gave weird results
    at times so I went back to my original approach of working with CHMs"""
import os.path # import os library for file path operations
import re # import Python RegEx library
import rasterio as rio # import library to read/write raster files

path = os.path.abspath('/media/becode/EXT/DSMsplit')
folder_path = path

"""walk trough folder with split DSMs, open them, then open corresponding DTM 
    and subtract both of them to create a CHM, lastly write CHM to file"""
for path, dirs, files in os.walk(folder_path):
    for file in files:
        if re.match("(.)+.tif", file) is not None: #check if it is a .tif file

            with rio.open(os.path.join(path, file)) as plot_dsm:
                dsm = plot_dsm.read(1, masked=True) # mask dsm to make sure we have no nodata values
                dsm.meta = plot_dsm.profile

            # change path to read in DTM based upon path DSM
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
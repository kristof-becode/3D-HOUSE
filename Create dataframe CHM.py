"""This .py file creates a csv from a Pandas Dataframe to index all the CHM files by path and bounds(boundaries),
being left, bottom,right, top coords of the map/raster. In this way it is possible to determine in which raster a file
a certain point with coords x,y Lambert72 would be included
"""

import os.path # import os library for file path operations
import re # import Python RegEx library
import rasterio as rio # import library to read/write raster files
import pandas as pd # Import Pandas dataframe library

# set display options for dataframes
pd.set_option('display.width',400)
pd.set_option('display.max_columns', 40)

path = os.path.abspath('/media/becode/EXT/CHMsplit') # set path
folder_path = path

name, left, bottom, right, top  = [], [], [], [], [] # define lists to read in raster data

for path, dirs, files in os.walk(folder_path):
    for file in files:
        if re.match("(.)+.tif", file) is not None: # check for .tif file
            with rio.open(os.path.join(path, file)) as plot_chm: # open and read CHM file
                chm = plot_chm.read(1)
            # append name and bounds coords to lists
            name.append(plot_chm.name)
            left.append(plot_chm.bounds[0])
            bottom.append(plot_chm.bounds[1])
            right.append(plot_chm.bounds[2])
            top.append(plot_chm.bounds[3])
            print(file) # follow progress
            plot_chm.close()
# create dataframe from lists
chm = pd.DataFrame({'filename' : name, 'left' : left,'bottom' : bottom,  'right' : right, 'top' : top })
print(chm.head(10))
chm.to_csv('/media/becode/EXT/CHMsplit/chm.csv') # write Dataframe out as csv file
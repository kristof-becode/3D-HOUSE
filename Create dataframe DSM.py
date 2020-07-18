import os.path
import re
import rasterio as rio
import pandas as pd
pd.set_option('display.width',400)
pd.set_option('display.max_columns', 40)

path = os.path.abspath('/media/becode/EXT/DSMsplit')
folder_path = path

#LookupDict = {}
name, left, bottom, right, top  = [], [], [], [], []

for path, dirs, files in os.walk(folder_path):
    for file in files:
        if re.match("(.)+.tif", file) is not None:
            with rio.open(os.path.join(path, file)) as plot_dsm:
                dsm = plot_dsm.read(1)
            name.append(plot_dsm.name)
            left.append(plot_dsm.bounds[0])
            bottom.append(plot_dsm.bounds[1])
            right.append(plot_dsm.bounds[2])
            top.append(plot_dsm.bounds[3])
            print(file)
            plot_dsm.close()
dsm = pd.DataFrame({'filename' : name, 'left' : left,'bottom' : bottom,  'right' : right, 'top' : top })
print(dsm.head(10))
dsm.to_csv('/media/becode/EXT/DSMsplit/dsm.csv')
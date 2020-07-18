import os.path
import re
import rasterio as rio
import pandas as pd

pd.set_option('display.width',400)
pd.set_option('display.max_columns', 40)



path = os.path.abspath('/media/becode/EXT/CHMsplit')
folder_path = path

#LookupDict = {}
name, left, bottom, right, top  = [], [], [], [], []

for path, dirs, files in os.walk(folder_path):
    for file in files:
        if re.match("(.)+.tif", file) is not None:
            with rio.open(os.path.join(path, file)) as plot_chm:
                chm = plot_chm.read(1)
            name.append(plot_chm.name)
            left.append(plot_chm.bounds[0])
            bottom.append(plot_chm.bounds[1])
            right.append(plot_chm.bounds[2])
            top.append(plot_chm.bounds[3])
            print(file)
            plot_chm.close()
chm = pd.DataFrame({'filename' : name, 'left' : left,'bottom' : bottom,  'right' : right, 'top' : top })
print(chm.head(10))
chm.to_csv('/media/becode/EXT/CHMsplit/chm.csv')
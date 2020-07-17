import os
import numpy as np
import pandas as pd
import descartes
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("white")
import geopandas as gpd
import rasterio as rio
import earthpy as et
import earthpy.plot as ep
import shapely
import plotly.graph_objects as go
from rasterio import Affine as A
from rasterio.warp import calculate_default_transform, reproject, Resampling

#dictionary chm's :
LookupDict = {}
for i in range(0,640):
    path_chm = "/home/becode/Documents/Tile_chm25/tile_chm25__" + str(i) + ".tif"
    with rio.open(path_chm) as plot_chm:
        chm = plot_chm.read(1)
    filename = "tile_chm25__" + str(i) + ".tif"
    LookupDict[filename] = plot_chm.bounds
print(LookupDict)

import requests
import json
address = "Sint-Janstraat 22, Paal"
req = requests.get(f"http://loc.geopunt.be/geolocation/location?q={address}&c=1",)
x = req.json()['LocationResult'][0]['Location']['X_Lambert72']
y = req.json()['LocationResult'][0]['Location']['Y_Lambert72']
print("x= ", x, " y= ",y)

for key,value in LookupDict.items():
    left = value[0]
    right = value[2]
    bottom = value[1]
    top = value[3]
    #print(value[0])
    if left<x<right and bottom<y<top:
        print(key)
        path_chm = "/home/becode/Documents/Tile_chm25/" + key
        print(key)
        with rio.open(path_chm) as plot_chm:
            chm = plot_chm.read(1)
        row, col = plot_chm.index(x, y)
        row1, col1 = row - 100, col - 100
        row2, col2 = row + 100, col + 100
        mat = chm[row1:row2, col1:col2]
print(mat.shape)
fig = go.Figure(data=[
    go.Surface(z=mat)

])

fig.show()

#print(mat.transform)
#rasterio.transform.xy()
"""
df = pd.DataFrame(mat[0:, 0:], index = [i for i in range(mat.shape[0])],
        columns = [i for i in range(mat.shape[1])])
print(df)
fig = go.Figure(data=[go.Mesh3d(x=df.columns, y=df.index, z=df.values, color='lightpink', opacity=1)])
fig.show()


        fig = go.Figure(data=[
            go.Surface(z=mat)

        ])

        fig.show()
        #ep.plot_bands(mat, title="CHM", cmap="viridis")
        #plt.show()
    #else:
        #print("NO!")
"""
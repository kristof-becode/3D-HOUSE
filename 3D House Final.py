"""PLOTTING A 3D HOUSE FROM AN ADDRESS IN FLANDERS
"""

"""IMPORT LIBRARIES
"""
#import os # Library for file handling and paths
import numpy as np # Import numpy array library and numpy mask
import numpy.ma as ma # Import numpy mask
import pandas as pd # Import Pandas dataframe library

import rasterio as rio # Import Rasterio, a library for working with geospatial raster data
from rasterio.mask import mask # to mask or clip functionality
#from rasterio.plot import show # functionality to plot
from shapely.geometry import Polygon # Import Shapely to work with polygons

import requests # import requests library for making requests to websites
import re # import Python RegEx library

import plotly.graph_objects as go # Import Plotly library for 3D plotting
# Importing Typing Libraries
from typing import Dict
from typing import List
from typing import Union
from typing import Tuple

"""FUNCTIONS
"""
# Retrieve Lambert72 coordinates from API loc.geopunt.be, Lambert72 is used in all Flemish projections we'll use
def retrieve_coords(address : str) -> Tuple[float,float]:
    req = requests.get(f"http://loc.geopunt.be/geolocation/location?q={address}&c=1")
    x = req.json()['LocationResult'][0]['Location']['X_Lambert72']
    y = req.json()['LocationResult'][0]['Location']['Y_Lambert72']
    print("-> Lambert72 coords of provided address: \n x= ", x, " y= ", y)
    return x, y

"""Retrieve correct Canopy Height Model map to mask with polygon of house shape
If coords on edges of map, then create a suitable map with adjacent ones => no time left for this
"""
def retrieve_map(x : float,y : float) -> str:
    """Create Pandas dataframe from csv file that indexes all splitted CHM raster files and their path, then look
    for the file that contains my x,y Lambert72 coords and return the path from the dataframe
    """
    maps = pd.read_csv('/media/becode/EXT/CHMsplit/chm.csv', sep=',')
    maps = maps.filename[(maps.left < x) & (x < maps.right) & (maps.bottom < y) & (y < maps.top)]
    path_open = maps.iloc[0]
    print('-> map retrieved from : ', path_open)
    return path_open

# def createCHM(x,y): in case of on edge of map => no time for this feature

"""Retrieve polygon(or house ground layer dimensions) from API : https://api.basisregisters.dev-vlaanderen.be
Only one polygon found per 'perceel' so that should be the main building (sheds etc are not in the polygon lists)
I also calculate area, total length(house circumference) of polygon
"""
def retrieve_polygon(address : str) -> List[Dict[str,List[float]]]:
    result = re.search("^([A-z- ]+)([0-9]+[A-z]?),[ ]?([0-9]+)[ ]?([A-z]+)", address)
    street = result.group(1)
    nb = result.group(2)
    pc = result.group(3)
    city = result.group(4)
    """Request polygon from API : https://api.basisregisters.dev-vlaanderen.be/v1/percelen/{objectId} 
    and retrieve .json object
    """
    req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/adresmatch?gemeentenaam={city}&straatnaam={street}&huisnummer={nb}&postcode={pc}").json()
    objectId = req["adresMatches"][0]["adresseerbareObjecten"][0]["objectId"]
    req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/gebouweenheden/{objectId}").json()
    objectId = req["gebouw"]["objectId"]
    req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/gebouwen/{objectId}").json()
    polygon = [req["geometriePolygoon"]["polygon"]]
    return polygon

# Using the polygon from retrievePolygon and CHM from retrieveCHM, I mask the polygon from CHM raster to create mask
def mask_polygon(poly : List[Dict[str,List[float]]] , path : str) -> np.ndarray:
    """Open path of CHM to mask polygon shape from. The polygon is a function parameter as well and is used in the
    mask function as a shape to mask by
    """
    path_chm = path
    map_chm = rio.open(path_chm)
    """Mask or clip the polygon shape from the CHM raster data with rasterio mask function, this returns a 
    masked raster file and a transform
    """
    mask_chm, mask_chm_transform = mask(dataset=map_chm, shapes=poly, crop=True, nodata=0, filled=True, indexes=1)
    print('-> mask succesful')
    return mask_chm

# With the polygon shape and the masked image/map we can calculate dimensions of the house
def dim_house(poly : List[Dict[str,List[float]]] , mask_chm: np.ndarray) -> Dict[str, Union[float, int]] :
    """Create polygon shape with Shapely function Polygon from coordinates of polygon list
    """
    polygon = Polygon(poly[0]['coordinates'][0])
    """I need to exclude 0 values from my masked CHM array to calculate a mean height  so I use numpy mask for masking
     the 0's and hereby create the array 'noZeros', sonp.mean(noZeros) will calculate mean height
    """
    noZeros = ma.masked_values(mask_chm, 0)
    """Create dict with house dimensions: area of ground floor, circumference, mean height(see above), max height 
    and possible floors
    """
    dimensions = {"area[m2] : " : round(polygon.area,1), "circumference[m] : ": round(polygon.length,1),
                  "mean height[m] : " : round(ma.mean(noZeros),1), "max height[m] : " : round(np.max(mask_chm),1),
                  "floors : " : int((np.max(mask_chm) // 3))}
    print('-> house dimensions:')
    for key,value in dimensions.items():
        print(key, value)
    return dimensions

# This function plots the masked CHM and prints out the house dimension details
def D3Plot(address : str, mask : np.ndarray, dimensions : Dict[str, Union[float, int]] ) -> None:
    # plots a surface plot of the mask from polygon out of CHM
    fig = go.Figure(data=[go.Surface(z=mask)])
    fig.update_layout(title='3D Plot of ' + address, width=750, height=750)
    fig.show()
    print("-> I hope you liked the 3D plot! \n")
    return

# MAIN
def main():
    # Welcome text and explanation of the programme
    print('\nIn this programme you can create a 3D plot of a house in Flanders.')
    print('Please use the following format for entering the address: Sint-janstraat 20, 3583 Beringen')
    # Ask for user to input an address in Flanders in a valid format
    while True:
        try:
            address = input('-> Please provide an address (or "q" to quit) : ')
            if re.match("^([A-z-]+)\s([0-9]+[A-z]?),\s([0-9]+)\s([A-z]+)", address): # RegEx to verify format
                print('-> valid address format')

                # retrieve Lambert72 x,y coordinates for the provided address
                x, y = retrieve_coords(address)

                # retrieve path of map (or raster) to mask from later (path derived from Lambert72 x,y coords)
                chm = retrieve_map(x,y)

                polygon = retrieve_polygon(address)  # retrieve polygon(coords) of house from address

                # mask polygon from Canopy Height Model raster (starting from polygon and CHM raster)
                mask = mask_polygon(polygon,chm)

                # from polygon and masked CHM calculate house dimensions(area, height, etc)
                dimensions = dim_house(polygon, mask)

                D3Plot(address, mask, dimensions)  # 3D surface plot of house from mask with Plotly

            elif address == 'q': # Hitting 'q' quits the programme
                print('Bye, thanks for plotting!')
                break
        except ValueError:
                print('-> Not a valid address format or something else went wrong!')
                continue

main()
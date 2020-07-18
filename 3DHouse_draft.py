"""IMPORT LIBRARIES"""

# Library for file handling and paths
import os
# Import numpy array library and numpy mask
import numpy as np
import numpy.ma as ma
# Import Pandas dataframe library
import pandas as pd
# Import Rasterio, a library for working with geospatial raster data
import rasterio as rio
# to mask or clip functionality
from rasterio.mask import mask
# functionality to plot
from rasterio.plot import show
# Import Shapely to work with polygons
from shapely.geometry import Polygon
# Library for making requests to websites
import requests
# Library RegEx
import re
#Library to work with json objects
import json
# Import Plotly library for 3D plotting
import plotly.graph_objects as go

"""FUNCTIONS"""

# Retrieve Lambert72 coordinates from loc.geopunt.be API, Lambert72 is used in all Flemish projections we'll use
def retrieveCoords(address : str) -> float:
    req = requests.get(f"http://loc.geopunt.be/geolocation/location?q={address}&c=1", )
    x = req.json()['LocationResult'][0]['Location']['X_Lambert72']
    y = req.json()['LocationResult'][0]['Location']['Y_Lambert72']
    print("Lambert72 coords of provided address: x= ", x, " y= ", y)
    return x,y

# Retrieve correct Canopy Height Model map to mask with polygon of house shape !!! OR DSM!!!
# If coords on edges of map, then create a suitable map with adjacent ones
def retrieveMap(x : float,y : float) -> str:
    """DSM
    maps = pd.read_csv('/media/becode/EXT/DSMsplit/dsm.csv', sep=',')
    maps = maps.filename[(maps.left < x) & (x < maps.right) & (maps.bottom < y) & (y < maps.top)]
    path_open = maps.iloc[0]
    print('-> map retrieved from : ', path_open)
    return path_open
    """
    maps = pd.read_csv('/media/becode/EXT/CHMsplit/chm.csv', sep=',')
    maps = maps.filename[(maps.left < x) & (x < maps.right) & (maps.bottom < y) & (y < maps.top)]
    path_open = maps.iloc[0]
    print('-> map retrieved from : ', path_open)
    return path_open

# OR def createCHM(x,y):

# Retrieve polygon(or house ground layer dimensions) from API : https://api.basisregisters.dev-vlaanderen.be
# Only one polygon found per 'perceel' so that should be the main building (sheds etc are not in the polygon lists)
# I also calculate area, total length(house circumference) of polygon
def retrievePolygon(address : str) -> list:
    #result = re.search("^([A-z-]+)\s(\d+),\s(\d+)\s([A-z]+)", address)
    result = re.search("^([A-z- ]+)(\d+[A-z]?),\s(\d+)\s([A-z]+)", address)
    street = result.group(1)
    nb = result.group(2)
    pc = result.group(3)
    city = result.group(4)
    # Request polygon from API : https://api.basisregisters.dev-vlaanderen.be/v1/percelen/{objectId} and retrieve .json object
    req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/adresmatch?gemeentenaam={city}&straatnaam={street}&huisnummer={nb}&postcode={pc}").json()

    objectId = req["adresMatches"][0]["adresseerbareObjecten"][0]["objectId"]
    req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/gebouweenheden/{objectId}").json()

    objectId = req["gebouw"]["objectId"]
    req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/gebouwen/{objectId}").json()

    polygon = [req["geometriePolygoon"]["polygon"]]
    #print("Polygon coords : ", polygon)
    # Get the coordinates of the polygon from list
    # create polygon from these coordinates with Shapely Polygon
    #poly = Polygon(polygon[0]['coordinates'][0])
    #print("Polygon coords : ", polygon[0]['coordinates'][0])
    #return polygon[0]['coordinates'][0]
    print(polygon)
    return polygon

# Using the polygon from retrievePolygon and CHM from retrieveCHM, I mask the polygon from CHM raster to create
#def maskPolygon(poly,CHM):
def maskPolygon(poly,path):
    # Get the coordinates of the polygon from list
    # create polygon from these coordinates with Shapely Polygon
    #P = Polygon(poly[0]['coordinates'][0])
    #Poly = Polygon(poly)
    # Read in the appropriate CHM file(or reconstructed one) with rasterio
    #path_chm = "/home/becode/Documents/Tile_chm25/tile_chm25__172.tif" # RECONSTRUCT PATH AFTER SPLITTING !!!!!
    path_chm = path
    map_chm = rio.open(path_chm)
    # mask or clip the polygon shape from the CHM raster data with rasterio mask function,
    # this returns a masked and a transform
    mask_chm, mask_chm_transform = mask(dataset=map_chm, shapes=poly, crop=True, nodata=0, filled=True, indexes=1)
    print('-> mask succesful \n')
    return mask_chm

# With the polygon shape and the masked image/map we can calculate dimensions of the house
def dimHouse(poly, mask_chm):
    # Get the coordinates of the polygon from list
    # create polygon from these coordinates with Shapely Polygon
    polygon = Polygon(poly[0]['coordinates'][0])
    # Now from masked CHM we calculate the mean height, therefore we need to exclude the zero values
    # I use numpy mask for masking the 0's and create the array 'noZeros'
    # np.mean(noZeros) will calculate mean height
    noZeros = ma.masked_values(mask_chm, 0)
    # Create a dictionary with all the dimensions: area of ground floor, circumerence, mean height(see before), max height and possible floors
    dimensions = {"area[m2] : " : round(polygon.area,1), "circumference[m] : ": round(polygon.length,1),
                  "mean height[m] : " : round(np.mean(noZeros),1), "max height[m] : " : round(np.max(mask_chm),1),
                  "floors : " : int((np.max(mask_chm) // 3))}
    for key,value in dimensions.items():
        print(key, value)
    return dimensions

# This function plots the masked CHM and prints out the house dimension details
def D3Plot(mask, dimensions):
    # plots a surface plot of the mask from polygon out of CHM
    fig = go.Figure(data=[go.Surface(z=mask)])
    #fig.update_layout(legend="area = " + str(polygon.area) + "circumference : " + str(polygon.length) + "mean height : " + str(
    #    np.mean(z)) + " max height : " + str(np.max(crop_chm_img)))
    fig.show()
    print("\n   I hope you enjoyed the plot!")
    return

# MAIN FUNC
def main():
    #Ask for user to input an address in Flanders in a valid format
    print('Below you can type an address in Flanders to plot the corresponding 3D House')
    print('Example: Sint-janstraat 20, 3583 Beringen')
    address = input('-> Please provide an address: ')
    # BELOW TRY / EXCEPTION
    #if (re.match('^([A-z-]+)\s(\d+),\s(\d+)\s([A-z]+)'), address):
        #print("Valid address")
    #else:
        #print("This address was not in the valid format.") # Hier aan pitsen dat als niet n input dan weer adres ingeven

    # FUNC TO RETRIEVE COORDS FROM ADDRESS : retrieve Lambert72 x,y coordinates for the provided address
    x,y = retrieveCoords(address)

    # FUNC TO SELECT CHM FROM ADDRESS, USES INPUT COORDS PREVIOUS FUNC - (LOOKUP FUNC) but also (CREATE VALID MAP AROUND COORDS)
    chm = retrieveMap(x,y)

    # FUNC TO RETRIEVE POLYGON TO CUT CHM (FROM API) - (RETRIEVE POLYGON COORDS) but also (LENGTH + AREA POL)
    polygon = retrievePolygon(address)

    # FUNC to MASK POLYGON FROM CHM MAP, USES POLYGON AND CHM
    mask = maskPolygon(polygon,chm)

    # FUNC TO CALCULATE HOUSE DIMENSION PARAMETERS
    dimensions = dimHouse(polygon, mask)

    # PLOT 3D HOUSE AND PRINT DETAILS(HEIGHT_MEAN/MAX, AREA, CIRCUMFERENCE)
    D3Plot(mask, dimensions)

main()
# NU RETRIEVEMAP RETUrn PATH MAAR BIJ NODIG ALS NIZUWE MAP MAKEN DAN BETER TIETS ANDERS OF EVRWIJZEN NAAR ANDERE FIE
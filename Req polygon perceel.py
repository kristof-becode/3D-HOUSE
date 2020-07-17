import re
import requests

import os
import numpy as np
import numpy.ma as ma
import pandas as pd
import descartes
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("white")
import geopandas as gpd
import rasterio as rio
from rasterio.mask import mask
from rasterio.plot import show
from shapely.geometry import Polygon
import earthpy as et
import earthpy.plot as ep
import shapely
import plotly.graph_objects as go
from rasterio import Affine as A
from rasterio.warp import calculate_default_transform, reproject, Resampling

address = 'Diestersesteenweg 26, 3583 Beringen'
address_regx = re.compile("^([A-z-]+)\s(\d+),\s(\d+)\s([A-z]+)")
result = address_regx.search(address)
street = result.group(1)
nb = result.group(2)
pc = result.group(3)
city = result.group(4)

#https://api.basisregisters.dev-vlaanderen.be/v1/percelen/{objectId}
req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/adresmatch?gemeentenaam={city}&straatnaam={street}&huisnummer={nb}&postcode={pc}").json()

objectId = req["adresMatches"][0]["adresseerbareObjecten"][0]["objectId"]

req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/gebouweenheden/{objectId}").json()

objectId = req["gebouw"]["objectId"]

req = requests.get(f"https://api.basisregisters.dev-vlaanderen.be/v1/gebouwen/{objectId}").json()

polygon = [req["geometriePolygoon"]["polygon"]]
print(polygon)
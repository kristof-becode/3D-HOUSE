# 3D-House

A program to look up an address in Flanders, Belgium and render a 3D plot of the corresponding house.  An estimate of the surface area of the ground floor, the height and the possible number of floors is provided as well. 
This is the first program I wrote in Python as part of an AI Bootcamp training.

<table>
  <tr>
    <td><img src="https://github.com/kristof-becode/3D-House/blob/master/OLV.png" width=75% height=75%/></td>
    <td><img src="https://github.com/kristof-becode/3D-House/blob/master/Korenmarkt%2015.png" width=75% height=75%/></td>
    <td><img src="https://github.com/kristof-becode/3D-House/blob/master/Snoekstraat.png" width=75% height=75%/></td>
  </tr>
 </table>
 
 Python Libraries used:
* Numpy: scientific package
* Pandas: data exploration package
* Requests: library for making website requests
* Rasterio: library to work with geospatial raster data
* Shapely: library to work with shapes and polygons
* Plotly: plotting package
 
## How it works

### Gather data

Data was gathered from a government website that provides Digital Surface Models(DSM) and Digital Terrain Models(DTM) in GeoTiff format of the entire Flanders area. These files were processed from LIDAR plane data.

DSM files rerieved from:
http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dsm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DSM,%20raster,%201m

DTM files retrieved from:
http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dtm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DTM,%20raster,%201m


LiDAR or Light Detection and Ranging is an active remote sensing system that can be used to measure vegetation and other heights across wide areas. Often people work with lidar data in raster format given it’s smaller in size and thus easier to work with. 

The DSM represents the top of surfaces(trees, buildings..), while the DTM represents the ground surface elevation.

### Processing GeoTiff raster files

Tiling DSM and DTM raster files

These files were between several 100 Mb and over1 Gb in size so I was necessary to cut them into tiles for rendering and further processing. The code for this step can be found in 'Cut DSM.py' and 'Cut DTM.py' .

### Creating a Canopy Height Model(CHM)

Canopy Height Model (CHM): the height or residual distance between the ground and the top of the of objects above the ground. This includes the actual heights of trees, buildings and any other objects on the earth’s surface. This CHM is created by subtracting the DTM from the DSM. 

<img src="https://github.com/kristof-becode/3D-House/blob/master/lidarTree-height.png" align ="center" width=25% height=25%/>

The Canopy Height Model is calculated from the cut DSM and DTM tiles from previous step. The cut DTM is substacted from the corresponding cut DSM raster file and the resulting Canopy Height Model raster file is saved. From now on we will be only working with this file. The code for this processing step can be found in 'Create CHM.py' .

### Getting the coordinates of an address

We can get the coordinates of an address in Flanders by making a request from an API from the government: 
http://loc.geopunt.be/geolocation/location?q={address}&c=1

The resulting coordinates are in Lambert coordinates, the geospatial coordinate convention in Belgium, which matches the coordinates in the GeoTiff raster files.
Now that we can link an address to coordinates we can select the corresponding CHM file in which lies the house we would like to plot.

To this end we create a CSV file that lists all the CHM files and the coordinate region they represent, or more precisely lists the corresponding corners coordinates of the bounding box. The code to create this CSV file can be found in 'Create Dataframe CHM.py'

### Retrieving the house polygon from API

Next we retrieve a polygon shape of the house with an API call from https://api.basisregisters.dev-vlaanderen.be

From this polygon we can retrieve an area and circumference on ground level using the Shapely package. For code, see '3DHouse Final.py' .

### Creating mask from CHM with polygon shape

Now we can create a mask from the CHM with the polygon shape using the rasterio mask function. We have effectively cut out the shape of the house from the raster file based on the polygon. From this mask we can also retrieve the height of the house. For code, see '3DHouse Final.py' .

### 3D House Plot

We can plot a surface plot of this mask using Plotly and render the 3D house plot. We gathered estimates for height, ground flour area and circumference of the house in previous steps.

Et voilà!

<img src="https://github.com/kristof-becode/3D-House/blob/master/OLV.png" width=100% height=100%/>

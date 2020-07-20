"""This .py file cuts the downloaded Terrain Surface Model raster files in tiles of 1000m by 1000m
I found this code on stackoverflow and tweaked it to do what I needed it to do
"""
from shapely import geometry # import Shapely to work with bounding boxes
import rasterio as rio # import library to read/write raster files
from rasterio.mask import mask # to mask or clip functionality
# Takes a Rasterio dataset and splits it into squares of dimensions squareDim * squareDim
def splitImageIntoCells(img: np.ndarray, filename : str, squareDim : int) -> None:
    numberOfCellsWide = img.shape[1] // squareDim # divide # columns by new tile width
    numberOfCellsHigh = img.shape[0] // squareDim # divide # rows by new tile height
    x, y = 0, 0
    count = 0
    for hc in range(numberOfCellsHigh):
        y = hc * squareDim
        for wc in range(numberOfCellsWide):
            x = wc * squareDim
            geom = getTileGeom(img.transform, x, y, squareDim)
            getCellFromGeom(img, geom, filename, count)
            count = count + 1

# Generate a bounding box from the pixel-wise coordinates using the original datasets transform property
def getTileGeom(transform : np.ndarray, x : int, y : int, squareDim : int) -> Tuple(float):
    corner1 = (x, y) * transform
    corner2 = (x + squareDim, y + squareDim) * transform
    return geometry.box(corner1[0], corner1[1],
                        corner2[0], corner2[1])

# Crop the dataset using the generated box and write it out as a GeoTIFF
def getCellFromGeom(img : np.nda, geom : Tuple(float), filename : str, count : int) -> None:
    crop, cropTransform = mask(img, [geom], crop=True)
    writeImageAsGeoTIFF(crop,
                        cropTransform,
                        img.meta,
                        img.crs,
                        filename+"_"+str(count))

# Write the passed in dataset as a GeoTIFF
def writeImageAsGeoTIFF(img : np.ndarray, transform : np.ndarray, metadata : Dict[str,Union[str,int,np.ndarray]],
                        crs : str, filename : str) -> None:
    metadata.update({"driver":"GTiff",
                     "height":img.shape[1],
                     "width":img.shape[2],
                     "transform": transform,
                     "crs": crs})
    # FOR DTM : write tile to file
    with rio.open('/media/becode/EXT/DTMsplit/' +filename+'.tif', "w", **metadata) as dest:
        dest.write(img)

def main():
    for i in range(1,44): # loop to read in all 43 downloaded DTM raster files
        if i < 10 :
            path_in = "/media/becode/EXT/DTM/DHMVIIDTMRAS1m_k0" + str(i) + "/GeoTIFF/DHMVIIDTMRAS1m_k0" +str(i) + ".tif"
        else:
            path_in = "/media/becode/EXT/DTM/DHMVIIDTMRAS1m_k" + str(i) + "/GeoTIFF/DHMVIIDTMRAS1m_k" + str(
                i) + ".tif"
        plot_dtm = rio.open(path_in) # open raster file to read in
        splitImageIntoCells(plot_dtm, "tile_dtm_k" + str(i), 1000) #split specified raster file in 1000x1000 tiles
        print(i) # check progress

main()
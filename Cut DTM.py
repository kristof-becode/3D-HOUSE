from shapely import geometry
import rasterio as rio
from rasterio.mask import mask

# Takes a Rasterio dataset and splits it into squares of dimensions squareDim * squareDim
def splitImageIntoCells(img, filename, squareDim):
    numberOfCellsWide = img.shape[1] // squareDim
    numberOfCellsHigh = img.shape[0] // squareDim
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
def getTileGeom(transform, x, y, squareDim):
    corner1 = (x, y) * transform
    corner2 = (x + squareDim, y + squareDim) * transform
    return geometry.box(corner1[0], corner1[1],
                        corner2[0], corner2[1])

# Crop the dataset using the generated box and write it out as a GeoTIFF
def getCellFromGeom(img, geom, filename, count):
    crop, cropTransform = mask(img, [geom], crop=True)
    writeImageAsGeoTIFF(crop,
                        cropTransform,
                        img.meta,
                        img.crs,
                        filename+"_"+str(count))

# Write the passed in dataset as a GeoTIFF
def writeImageAsGeoTIFF(img, transform, metadata, crs, filename):
    metadata.update({"driver":"GTiff",
                     "height":img.shape[1],
                     "width":img.shape[2],
                     "transform": transform,
                     "crs": crs})
    # FOR DSM
    with rio.open('/media/becode/EXT/DTMsplit/' +filename+'.tif', "w", **metadata) as dest:
        dest.write(img)

def main():
    for i in range(1,44):
        if i < 10 :
            path_in = "/media/becode/EXT/DTM/DHMVIIDTMRAS1m_k0" + str(i) + "/GeoTIFF/DHMVIIDTMRAS1m_k0" +str(i) + ".tif"
        else:
            path_in = "/media/becode/EXT/DTM/DHMVIIDTMRAS1m_k" + str(i) + "/GeoTIFF/DHMVIIDTMRAS1m_k" + str(
                i) + ".tif"
        plot_dtm = rio.open(path_in)
        splitImageIntoCells(plot_dtm, "tile_dtm_k" + str(i), 1000)
        print(i)

main()
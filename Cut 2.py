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
    # FOR DSM, DTM below
    #with rio.open('/home/becode/Documents/Tile_dsm25' + filename + '.tif', "w", **metadata) as dest:
        #dest.write(img)
    with rio.open('/home/becode/Documents/Tile_dtm25/' +filename+'.tif', "w", **metadata) as dest:
        dest.write(img)

def main():

    # For DSM, DTM below
    #plot_dsm = rio.open('/home/becode/Documents/DSM k25/GeoTIFF/DHMVIIDSMRAS1m_k25.tif')
    #dsm = plot_dsm.read(1)
    plot_dtm = rio.open('/home/becode/Documents/DTM k25/GeoTIFF/DHMVIIDTMRAS1m_k25.tif')
    dtm = plot_dtm.read(1)


    splitImageIntoCells(plot_dtm, "tile_dtm25_", 1000)

main()
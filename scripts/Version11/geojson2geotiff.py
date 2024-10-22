import rasterio
from rasterio.features import rasterize
import geopandas as gpd
import numpy as np
from shapely.geometry import box

class GeoJSONToGeoTIFFConverter:
    def __init__(self, input_geojson, output_geotiff):
        self.input_geojson = input_geojson
        self.output_geotiff = output_geotiff

    def convert(self):
        # Load the GeoJSON file using Geopandas
        gdf = gpd.read_file(self.input_geojson)

        # Set the CRS to EPSG:4326
        gdf = gdf.set_crs("EPSG:4326", allow_override=True)

        # Check the bounding box of the geometries
        bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
        print("Bounding Box:", bounds)

        # Create a bounding box geometry in EPSG:4326 with a buffer
        buffer_size = 0.00001  # Adjust this value if necessary to expand the bounding box
        bbox_geom = gpd.GeoSeries([box(bounds[0] - buffer_size, bounds[1] - buffer_size, 
                                        bounds[2] + buffer_size, bounds[3] + buffer_size)]).set_crs("EPSG:4326")

        # Get the bounds in the same CRS
        projected_bounds = bbox_geom.total_bounds
        print("Projected Bounds:", projected_bounds)

        # Calculate output raster shape and transform based on the bounding box
        out_shape = (32000, 32000)  # Adjust this for desired resolution
        transform = rasterio.transform.from_origin(
            west=projected_bounds[0], 
            north=projected_bounds[3], 
            xsize=(projected_bounds[2] - projected_bounds[0]) / out_shape[1], 
            ysize=(projected_bounds[3] - projected_bounds[1]) / out_shape[0]
        )

        # Check raster bounds
        raster_bounds = [transform[2], transform[5], transform[2] + transform[0] * out_shape[1], transform[5] + transform[4] * out_shape[0]]
        print("Raster Bounds:", raster_bounds)

        # Use original geometries since they are already in EPSG:4326
        buffered_geometries = gdf.geometry

        # Rasterize the geometries in EPSG:4326
        out_raster = rasterize(
            [(geom, 255) for geom in buffered_geometries],
            out_shape=out_shape,
            transform=transform,
            fill=0,
            all_touched=True
        )

        # Define metadata for the output GeoTIFF, including EPSG:4326
        metadata = {
            'driver': 'GTiff',
            'count': 1,
            'dtype': 'uint8',
            'width': out_shape[1],
            'height': out_shape[0],
            'crs': 'EPSG:4326',
            'transform': transform,
            'compress': 'deflate',
        }

        # Write the rasterized data to a GeoTIFF file
        with rasterio.open(self.output_geotiff, 'w', **metadata) as dst:
            dst.write(out_raster, 1)

# geojson_converter.py
import geopandas as gpd
from pyproj import Transformer
import json

class GeoJSONConverter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.transformer = Transformer.from_crs("EPSG:2056", "EPSG:4326", always_xy=True)

    def transform_coordinates(self, geometry):
        """Transform coordinates from LV95 to WGS84."""
        if geometry['type'] == 'Point':
            x, y = geometry['coordinates']
            lon, lat = self.transformer.transform(x, y)
            return {'type': 'Point', 'coordinates': [lon, lat]}
        elif geometry['type'] == 'LineString':
            coords = [self.transformer.transform(x, y) for x, y in geometry['coordinates']]
            return {'type': 'LineString', 'coordinates': [[lon, lat] for lon, lat in coords]}
        elif geometry['type'] == 'Polygon':
            coords = [[self.transformer.transform(x, y) for x, y in ring] for ring in geometry['coordinates']]
            return {'type': 'Polygon', 'coordinates': [[[lon, lat] for lon, lat in ring] for ring in coords]}
        else:
            return geometry  # Handle other geometry types as needed

    def convert(self):
        """Convert GeoJSON file from LV95 to WGS84."""
        # Read the input GeoJSON file
        gdf = gpd.read_file(self.input_file)

        # Transform the geometries and build the output structure
        features = []
        for _, row in gdf.iterrows():
            transformed_geom = self.transform_coordinates(row['geometry'].__geo_interface__)
            properties = row.drop('geometry').to_dict()
            features.append({
                "type": "Feature",
                "geometry": transformed_geom,
                "properties": properties
            })

        # Create the output GeoJSON structure
        output_geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        # Save the transformed GeoDataFrame to a new GeoJSON file
        with open(self.output_file, 'w') as f:
            json.dump(output_geojson, f, separators=(',', ':'), indent=None)

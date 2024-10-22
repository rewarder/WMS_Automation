from geojson2geotiff import GeoJSONToGeoTIFFConverter

def main():
    converter = GeoJSONToGeoTIFFConverter(
        input_geojson='modified_splines_WGS84.geojson',
        output_geotiff='modified_splines_WGS84.tif'
    )
    converter.convert()

if __name__ == "__main__":
    main()

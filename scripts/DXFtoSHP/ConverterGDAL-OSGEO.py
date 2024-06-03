from osgeo import ogr

def convert_dxf_to_shp(dxf_file, shp_file):
    # Get the input data source
    input_ds = ogr.Open(dxf_file)
    
    # Check if the file was successfully opened
    if input_ds is None:
        print(f"Failed to open file: {dxf_file}")
        return
    
    # Get the DXF layer
    layer = input_ds.GetLayer()
    
    # Create the output data source (Shapefile)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    output_ds = driver.CreateDataSource(shp_file)
    
    # Create the output layer
    output_layer = output_ds.CreateLayer(layer.GetName(), geom_type=layer.GetGeomType())
    
    # Copy features from the input layer to the output layer
    for feature in layer:
        output_layer.CreateFeature(feature.Clone())
    
    # Cleanup
    del input_ds, output_ds

if __name__ == "__main__":
    dxf_file = 'path/to/your/file.dxf'
    shp_dir = 'path/to/your/output_directory'
    shp_file = f'{shp_dir}/output_filename.shp'
    
    convert_dxf_to_shp(dxf_file, shp_file)

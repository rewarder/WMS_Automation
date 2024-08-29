import xml.etree.ElementTree as ET
import numpy as np
import rasterio
from rasterio.transform import from_origin

def parse_landxml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespaces = {'landxml': 'http://www.landxml.org/schema/LandXML-1.2'}

    surfaces = []

    for surface in root.findall('.//landxml:Surface', namespaces):
        points = []
        for p in surface.findall('.//landxml:P', namespaces):
            coords = list(map(float, p.text.split()))
            points.append(coords)
        
        faces = []
        for f in surface.findall('.//landxml:F', namespaces):
            face_indices = list(map(int, f.text.split()))
            # Convert 1-based index to 0-based index
            face = [points[i - 1] for i in face_indices]
            faces.append(face)

        surfaces.append((points, faces))
    
    return surfaces

def create_geotiff(points, output_path, pixel_size=0.5):
    # Get the min and max coordinates
    points = np.array(points)
    min_x, min_y = points[:, 0].min(), points[:, 1].min()
    max_x, max_y = points[:, 0].max(), points[:, 1].max()

    # Create a grid based on the points
    grid_shape = ((int((max_y - min_y) / pixel_size) + 1), (int((max_x - min_x) / pixel_size) + 1))
    elevation_grid = np.full(grid_shape, np.nan)

    for x, y, z in points:
        grid_x = int((x - min_x) / pixel_size)
        grid_y = int((max_y - y) / pixel_size)  # Invert y for proper orientation
        elevation_grid[grid_y, grid_x] = z

    # Define the transform for rasterio
    transform = from_origin(min_x, max_y, pixel_size, pixel_size)

    # Write the GeoTIFF file
    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=elevation_grid.shape[0],
        width=elevation_grid.shape[1],
        count=1,
        dtype='float32',
        crs='EPSG:2056',  # Adjust CRS as needed
        transform=transform,
    ) as dst:
        dst.write(elevation_grid, 1)

def main():
    landxml_file = 'Export_for_TEDAMOS_DGM.xml'  # Replace with your LandXML file path
    output_tiff_file = 'output_file.tif'  # Desired output GeoTIFF file path
    
    surfaces = parse_landxml(landxml_file)
    
    for i, (points, faces) in enumerate(surfaces, start=1):
        create_geotiff(points, f"{output_tiff_file[:-4]}_surface_{i}.tif")
        print(f"Surface {i} faces: {faces}")  # Optional: print faces for verification

if __name__ == "__main__":
    main()

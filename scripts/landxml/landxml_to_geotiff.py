import xml.etree.ElementTree as ET
import numpy as np
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import Polygon
from rasterio.features import rasterize

def parse_landxml(file_path):
    # Parse the LANDXML file to extract point and face data
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define namespace
    ns = {'ns': 'http://www.landxml.org/schema/LandXML-1.2'}

    # Extract points and faces from all surfaces
    points = []
    faces = []

    for surface in root.findall(".//ns:Surface", ns):
        # Extract points for the current surface
        for p in surface.findall(".//ns:Pnts/ns:P", ns):
            coords = p.text.split()
            if len(coords) == 3:
                x, y, z = map(float, coords)
                points.append((x, y, z))
            else:
                print("Unexpected point format:", p.text)

        # Extract faces for the current surface
        surface_faces = []
        for f in surface.findall(".//ns:Faces/ns:F", ns):
            indices = list(map(int, f.text.split()))
            surface_faces.append(indices)

        faces.extend(surface_faces)

    if not points:
        print("No points found. Check the XML structure and path.")
    
    return points, faces

def create_geotiff(points, faces, output_path, raster_width=100, raster_height=100):
    if not points:
        raise ValueError("No points to process.")

    xs, ys, zs = zip(*points)

    # Create a 2D grid with the elevation data
    grid = np.zeros((raster_height, raster_width))
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    x_resolution = (x_max - x_min) / raster_width
    y_resolution = (y_max - y_min) / raster_height

    # Rasterize points to the grid
    for x, y, z in points:
        x_idx = min(int((x - x_min) / x_resolution), raster_width - 1)
        y_idx = min(int((y - y_min) / y_resolution), raster_height - 1)
        grid[y_idx, x_idx] = z

    # Create polygons from faces and calculate average height for each face
    polygons = []
    for face in faces:
        if all(index < len(points) for index in face):  # Ensure indices are valid
            polygon_points = [points[index] for index in face]
            polygon = Polygon(polygon_points)

            # Calculate the average height of the face
            avg_height = np.mean([points[index][2] for index in face])
            polygons.append((polygon, avg_height))  # Use average height as value

    # Rasterize the polygons with average heights
    shapes = [(polygon, value) for polygon, value in polygons]
    rasterized_faces = rasterize(
        shapes,
        out_shape=grid.shape,
        transform=from_origin(x_min, y_max, x_resolution, y_resolution),
        fill=0,  # Fill value for pixels outside the polygons
        dtype='float32'
    )

    # Combine rasterized faces with point grid
    grid = np.maximum(grid, rasterized_faces)

    # Convert to uint8 (you can choose to keep it float32 if needed)
    grid = grid.astype(np.uint8)

    # Create a transform for the raster
    transform = from_origin(x_min, y_max, x_resolution, y_resolution)

    # Write the data to a GeoTIFF file
    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=raster_height,
        width=raster_width,
        count=1,
        dtype=grid.dtype,
        crs='EPSG:2056',
        transform=transform,
    ) as dst:
        dst.write(grid, 1)

# Use the functions
landxml_file_path = 'Export_for_TEDAMOS_DGM.xml'
output_geotiff_path = 'output_geotiff_file.tif'

# Increase these values for higher resolution
raster_width = 2000
raster_height = 2000

# Parse the LANDXML file
points, faces = parse_landxml(landxml_file_path)

# Create the GeoTIFF using normalized points
create_geotiff(points, faces, output_geotiff_path, raster_width, raster_height)

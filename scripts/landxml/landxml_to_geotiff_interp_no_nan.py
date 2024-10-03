import xml.etree.ElementTree as ET
import numpy as np  
import rasterio
from rasterio.transform import from_origin
from tqdm import tqdm
import time

def parse_landxml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespaces = {'landxml': 'http://www.landxml.org/schema/LandXML-1.2'}

    surfaces = []

    for surface in root.findall('.//landxml:Surface', namespaces):
        points = []
        for p in surface.findall('.//landxml:P', namespaces):
            # Split the coordinates and rearrange them to 'y, x, z'
            coords = list(map(float, p.text.split()))
            points.append([coords[1], coords[0], coords[2]])  # Switch x and y
            
        faces = []
        for f in surface.findall('.//landxml:F', namespaces):
            face_indices = list(map(int, f.text.split()))
            face = [points[i - 1] for i in face_indices]
            faces.append(face)

        surfaces.append((points, faces))
    
    return surfaces

def interpolate_triangle(p1, p2, p3, num_points):
    # Create a grid of points within the triangle
    points = []
    for i in range(num_points + 1):
        for j in range(num_points + 1 - i):
            alpha = i / num_points
            beta = j / num_points
            gamma = 1 - alpha - beta
            if gamma >= 0:  # Ensure the point is inside the triangle
                x = alpha * p1[0] + beta * p2[0] + gamma * p3[0]
                y = alpha * p1[1] + beta * p2[1] + gamma * p3[1]
                z = alpha * p1[2] + beta * p2[2] + gamma * p3[2]
                points.append([x, y, z])
    return points

def create_geotiff(points, output_path, pixel_size=0.15):
    points = np.array(points)
    
    # Filter out points with NaN values
    points = points[~np.isnan(points).any(axis=1)]

    min_x, min_y = points[:, 0].min(), points[:, 1].min()
    max_x, max_y = points[:, 0].max(), points[:, 1].max()

    grid_shape = (
        (int((max_y - min_y) / pixel_size) + 1),
        (int((max_x - min_x) / pixel_size) + 1)
    )
    elevation_grid = np.full(grid_shape, np.nan)

    for x, y, z in points:
        grid_x = int((x - min_x) / pixel_size)
        grid_y = int((max_y - y) / pixel_size)
        elevation_grid[grid_y, grid_x] = z

    transform = from_origin(min_x, max_y, pixel_size, pixel_size)

    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=elevation_grid.shape[0],
        width=elevation_grid.shape[1],
        count=1,
        dtype='float32',
        crs='EPSG:2056',
        transform=transform,
        compress='lzw'  # Add compression
    ) as dst:
        dst.write(elevation_grid, 1)

def save_points_to_txt(points, output_path):
    with open(output_path, 'w') as f:
        for point in points:
            f.write(f"{point[0]}, {point[1]}, {point[2]}\n")

def main():
    start_time = time.time() # Start the timer

    landxml_file = '1012_Model_Baugrube_wms.xml'
    output_tiff_file = '1012_Model_Baugrube_wms.tif'

    surfaces = parse_landxml(landxml_file)
    
    all_combined_points = []

    total_faces = sum(len(faces) for _, faces in surfaces)  # Total faces for progress tracking
    with tqdm(total=len(surfaces) + total_faces, desc="Processing All Surfaces") as pbar:
        for i, (points, faces) in enumerate(surfaces, start=1):
            interpolated_points = []
            for face in faces:
                if len(face) == 3:
                    interpolated_points.extend(interpolate_triangle(face[0], face[1], face[2], num_points=150))
                    interpolated_points.extend(face)

                pbar.update(1)  # Update progress for each face

            all_points = points + interpolated_points
            all_combined_points.extend(all_points)
            
            create_geotiff(all_points, f"{output_tiff_file[:-4]}_surface_{i}.tif")

            pbar.update(1)  # Update progress for each surface

    end_time = time.time() # End the timer
    execution_time = end_time - start_time

    # Save the execution time to a text file
    with open('execution_time_perf_opt.txt', 'w') as f:
        f.write(f"Total execution time: {execution_time:.2f} seconds\n")

if __name__ == "__main__":
    main()

import os
import xml.etree.ElementTree as ET
import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.merge import merge
from concurrent.futures import ProcessPoolExecutor

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
            face = [points[i - 1] for i in face_indices]
            faces.append(face)

        surfaces.append((points, faces))
    
    return surfaces

def interpolate_triangle(p1, p2, p3, num_points):
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

def interpolate_triangle_multithreaded(faces, num_points):
    with ProcessPoolExecutor() as executor:  # Use ProcessPoolExecutor
        futures = [executor.submit(interpolate_triangle, face[0], face[1], face[2], num_points) for face in faces]
        results = []
        for future in futures:
            results.extend(future.result())
    return results

def create_geotiff(points, output_path, pixel_size=0.14):
    points = np.array(points)
    min_x, min_y = points[:, 0].min(), points[:, 1].min()
    max_x, max_y = points[:, 0].max(), points[:, 1].max()

    grid_shape = ((int((max_y - min_y) / pixel_size) + 1), (int((max_x - min_x) / pixel_size) + 1))
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
    ) as dst:
        dst.write(elevation_grid, 1)

    return elevation_grid  # Return the elevation grid for further processing

def save_matrix_to_txt(matrix, output_txt_path):
    np.savetxt(output_txt_path, matrix, fmt='%.6f')  # Save matrix with 6 decimal places

def create_geotiff_multithreaded(all_points, output_path, pixel_size=0.14):
    num_cores = os.cpu_count()
    points_per_core = np.array_split(all_points, num_cores)
    part_files = []

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(create_geotiff, points, f"{output_path}_part_{i}.tif", pixel_size) for i, points in enumerate(points_per_core)]
        results = [future.result() for future in futures]
        part_files = [f"{output_path}_part_{i}.tif" for i in range(num_cores)]

    # Merge all part files into one final .tif
    src_files_to_mosaic = [rasterio.open(fp) for fp in part_files]
    mosaic, out_trans = merge(src_files_to_mosaic)

    # Write the mosaic to a single .tif file
    final_output_path = f"{output_path}.tif"
    with rasterio.open(
        final_output_path,
        'w',
        driver='GTiff',
        height=mosaic.shape[1],  # Correct height
        width=mosaic.shape[2],    # Correct width
        count=1,
        dtype='float32',
        crs='EPSG:2056',
        transform=out_trans,
    ) as dst:
        dst.write(mosaic.squeeze(), 1)  # Use squeeze() to remove single-dimensional entries

    # Close the individual files
    for src in src_files_to_mosaic:
        src.close()

    # Delete the part files
    for part in part_files:
        os.remove(part)

    return final_output_path  # Return the path of the final .tif file

def main():
    landxml_file = 'Export_for_TEDAMOS_DGM.xml'  # Replace with your LandXML file path
    output_tiff_file = 'output_file9.tif'  # Desired output GeoTIFF file path
    
    surfaces = parse_landxml(landxml_file)
    
    for i, (points, faces) in enumerate(surfaces, start=1):
        interpolated_points = []
        triangulated_faces = [face for face in faces if len(face) == 3]  # Ensure it's a triangle

        interpolated_points = interpolate_triangle_multithreaded(triangulated_faces, num_points=200)

        all_points = points + interpolated_points
        
        output_tiff_path = f"{output_tiff_file[:-4]}_surface_{i}"  # Base path for output files
        final_output_path = create_geotiff_multithreaded(all_points, output_tiff_path)  # Call the multithreaded function
        
        # Save the elevation grid to a .txt file for the last surface (or combine as needed)
        # output_txt_path = f"{output_tiff_file[:-4]}_surface_{i}.txt"
        # save_matrix_to_txt(elevation_grids[-1], output_txt_path)  # Save the last grid

        print(f"Surface {i} faces: {faces}")  # Optional: print faces for verification
        print(f"Final output saved to: {final_output_path}")

if __name__ == "__main__":
    main()

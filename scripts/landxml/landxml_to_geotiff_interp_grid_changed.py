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

def create_geotiff(points, output_path, pixel_size=0.14):
    points = np.array(points)
    min_x, min_y = points[:, 0].min(), points[:, 1].min()
    max_x, max_y = points[:, 0].max(), points[:, 1].max()

    grid_shape = ((int((max_x - min_x) / pixel_size) + 1), (int((max_y - min_y) / pixel_size) + 1))
    elevation_grid = np.full(grid_shape, np.nan)

    for x, y, z in points:
        grid_x = int((x - min_x) / pixel_size)
        grid_y = int((y - min_y) / pixel_size)
        elevation_grid[grid_x, grid_y] = z

    transform = from_origin(min_x, min_y, pixel_size, pixel_size)

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

def main():
    landxml_file = 'Export_for_TEDAMOS_DGM.xml'  # Replace with your LandXML file path
    output_tiff_file = 'Attisholzareal.tif'  # Desired output GeoTIFF file path
    
    surfaces = parse_landxml(landxml_file)
    
    for i, (points, faces) in enumerate(surfaces, start=1):
        interpolated_points = []
        for face in faces:
            if len(face) == 3:  # Ensure it's a triangle
                interpolated_points.extend(interpolate_triangle(face[0], face[1], face[2], num_points=200))

        all_points = points + interpolated_points
        
        output_tiff_path = f"{output_tiff_file[:-4]}_surface_{i}.tif"
        elevation_grid = create_geotiff(all_points, output_tiff_path)

        # Save the elevation grid to a .txt file
        output_txt_path = f"{output_tiff_file[:-4]}_surface_{i}.txt"
        save_matrix_to_txt(elevation_grid, output_txt_path)

        print(f"Surface {i} faces: {faces}")  # Optional: print faces for verification

if __name__ == "__main__":
    main()

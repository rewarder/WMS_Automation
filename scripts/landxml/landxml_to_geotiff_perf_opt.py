import xml.etree.ElementTree as ET
import numpy as np  
import rasterio
from rasterio.transform import from_origin
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
import time

def parse_landxml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {'landxml': 'http://www.landxml.org/schema/LandXML-1.2'}
    surfaces = []

    for surface in root.findall('.//landxml:Surface', namespaces):
        points = []
        for p in surface.findall('.//landxml:P', namespaces):
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
    a = np.array(p1)
    b = np.array(p2)
    c = np.array(p3)

    alpha = np.linspace(0, 1, num_points + 1)
    beta = np.linspace(0, 1, num_points + 1)
    alpha, beta = np.meshgrid(alpha, beta)
    gamma = 1 - alpha - beta

    inside = gamma >= 0
    x = alpha * a[0] + beta * b[0] + gamma * c[0]
    y = alpha * a[1] + beta * b[1] + gamma * c[1]
    z = alpha * a[2] + beta * b[2] + gamma * c[2]

    return np.column_stack((x[inside], y[inside], z[inside]))

def create_geotiff(points, output_path, pixel_size=0.07):
    points = np.array(points)
    points = points[~np.isnan(points).any(axis=1)]

    min_x, min_y = points[:, 0].min(), points[:, 1].min()
    max_x, max_y = points[:, 0].max(), points[:, 1].max()

    length_x = max_x - min_x
    length_y = max_y - min_y

    print(f"Bounding box dimensions: Length in X (meters): {length_x:.2f}, Length in Y (meters): {length_y:.2f}")

    grid_shape = (
        int((max_y - min_y) / pixel_size) + 1,
        int((max_x - min_x) / pixel_size) + 1
    )
    elevation_grid = np.full(grid_shape, np.nan)

    grid_x = ((points[:, 0] - min_x) / pixel_size).astype(int)
    grid_y = ((max_y - points[:, 1]) / pixel_size).astype(int)

    elevation_grid[grid_y, grid_x] = points[:, 2]

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
        compress='lzw'
    ) as dst:
        dst.write(elevation_grid, 1)

def calculate_triangle_area(p1, p2, p3):
    a = np.array(p2) - np.array(p1)
    b = np.array(p3) - np.array(p1)
    return 0.5 * np.linalg.norm(np.cross(a, b))

def calculate_triangle_angles(p1, p2, p3):
    a = np.linalg.norm(p2 - p3)
    b = np.linalg.norm(p1 - p3)
    c = np.linalg.norm(p1 - p2)

    # Using the law of cosines to find the angles
    angle_A = np.arccos((b**2 + c**2 - a**2) / (2 * b * c))  # Angle at vertex A
    angle_B = np.arccos((a**2 + c**2 - b**2) / (2 * a * c))  # Angle at vertex B
    angle_C = np.arccos((a**2 + b**2 - c**2) / (2 * a * b))  # Angle at vertex C

    return np.degrees(angle_A), np.degrees(angle_B), np.degrees(angle_C)  # Convert to degrees

def find_flatest_triangle_and_smallest_angle(faces, points):
    flatness_scores = []
    smallest_angle_info = None
    largest_triangle_info = None

    for face in faces:
        if len(face) == 3:
            # Convert face points to numpy arrays
            p1, p2, p3 = np.array(face[0]), np.array(face[1]), np.array(face[2])
            
            # Calculate area and height difference
            area = calculate_triangle_area(p1, p2, p3)
            height_diff = np.max([p1[2], p2[2], p3[2]]) - np.min([p1[2], p2[2], p3[2]])

            if area > 0:  # Avoid division by zero
                flatness_score = height_diff / area
                flatness_scores.append((flatness_score, face))

            # Calculate angles
            angles = calculate_triangle_angles(p1, p2, p3)
            min_angle = min(angles)

            # Update smallest angle information
            if smallest_angle_info is None or min_angle < smallest_angle_info[0]:
                smallest_angle_area = area
                smallest_angle_info = (min_angle, face, smallest_angle_area)

            # Update largest triangle information
            if largest_triangle_info is None or area > largest_triangle_info[1]:
                largest_triangle_info = (face, area)

    # Find the triangle with the minimum flatness score
    flattest_triangle = None
    if flatness_scores:
        flatness_scores.sort(key=lambda x: x[0])  # Sort by flatness score
        flattest_triangle = flatness_scores[0]  # Return the flattest triangle

    return flattest_triangle, smallest_angle_info, largest_triangle_info

def determine_num_points(largest_triangle_area):
    # Base num_points primarily on the largest triangle area
    # base_points = file_size_kb // 50  # Start with a base derived from file size
    area_factor = largest_triangle_area / 3 # Scale based on largest triangle area

    # Calculate num_points
    num_points = int(area_factor)
    
    # Ensure a minimum and maximum number of points
    return max(100, min(num_points, 1000))

def split_large_triangle(p1, p2, p3):
    # Calculate the midpoint of the longest edge
    a, b, c = np.array(p1), np.array(p2), np.array(p3)
    edges = [(a, b), (b, c), (c, a)]
    edge_lengths = [np.linalg.norm(edge[0] - edge[1]) for edge in edges]
    longest_edge_index = np.argmax(edge_lengths)
    longest_edge = edges[longest_edge_index]

    midpoint = (longest_edge[0] + longest_edge[1]) / 2

    # Create two new triangles from the midpoint
    if longest_edge_index == 0:
        return [(a, midpoint, c), (b, midpoint, c)]
    elif longest_edge_index == 1:
        return [(b, midpoint, a), (c, midpoint, a)]
    else:
        return [(c, midpoint, b), (a, midpoint, b)]

def process_surface(surface, idx, output_tiff_file):
    points, faces = surface

    if not points or not faces:
        print(f"Surface {idx} has no points or faces, skipping.")
        return

    print(f"Processing Surface {idx} with {len(faces)} faces and {len(points)} points.")

    interpolated_points = []

    flattest_triangle, smallest_angle_triangle, largest_triangle = find_flatest_triangle_and_smallest_angle(faces, points)
    largest_triangle_area = largest_triangle[1] if largest_triangle else 0
    num_points = determine_num_points(largest_triangle_area)

    if flattest_triangle:
        flatness_score, face = flattest_triangle
        print(f"Surface {idx}: Flattest triangle with score {flatness_score:.4f} - Vertices: {face}")

    if smallest_angle_triangle:
        smallest_angle, face, area = smallest_angle_triangle
        print(f"Surface {idx}: Triangle with smallest angle {smallest_angle:.6f} degrees - Vertices: {face}, Area: {area:.6f}")

    if largest_triangle:
        face, area = largest_triangle
        print(f"Surface {idx}: Largest triangle - Vertices: {face}, Area: {area:.6f}")

    for face in faces:
        triangles_to_process = [face]
        
        while triangles_to_process:
            current_triangle = triangles_to_process.pop()
            if len(current_triangle) == 3:
                area = calculate_triangle_area(*current_triangle)
                if area > 1:
                    # Split the triangle and add new triangles to the list to process
                    new_triangles = split_large_triangle(*current_triangle)
                    triangles_to_process.extend(new_triangles)
                else:
                    # If the triangle is small enough, interpolate and add points
                    interpolated_points.extend(interpolate_triangle(*current_triangle, num_points))
                    interpolated_points.extend(current_triangle)

    all_points = points + interpolated_points
    create_geotiff(all_points, f"{output_tiff_file[:-4]}_surface_{idx}.tif")

def main():
    start_time = time.time()  # Start the timer

    # Example values for the files being processed
    test_files = [
        # {'file': 'blubb_for_testing.xml'},
        # {'file': 'Export_for_TEDAMOS_DGM_for_testing.xml'},
        {'file': '1012_Model_Baugrube_wms_for_testing.xml'}
    ]

    for test_file in test_files:
        landxml_file = test_file['file']
        output_tiff_file = landxml_file.replace('.xml', '.tif')
        
        surfaces = parse_landxml(landxml_file)
        
        with ProcessPoolExecutor() as executor:
            futures = []
            for i, surface in enumerate(surfaces, start=1):
                futures.append(executor.submit(process_surface, surface, i, output_tiff_file))
            
            # Retrieve results to ensure tasks are completed and capture any exceptions
            for future in tqdm(futures, desc="Processing surfaces"):
                try:
                    future.result()  # This will block until the future is done and raise any exceptions
                except Exception as e:
                    print(f"Error processing surface: {e}")

    end_time = time.time()  # End the timer
    execution_time = end_time - start_time

    # Save the execution time to a text file
    with open('execution_time_perf_opt.txt', 'w') as f:
        f.write(f"Total execution time: {execution_time:.2f} seconds\n")

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import xml.etree.ElementTree as ET
import numpy as np  
import rasterio
from rasterio.crs import CRS 
from rasterio.transform import from_origin
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

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

def create_geotiff(points, output_path, pixel_size):
    points = np.array(points)
    points = points[~np.isnan(points).any(axis=1)]

    min_x, min_y = points[:, 0].min(), points[:, 1].min()
    max_x, max_y = points[:, 0].max(), points[:, 1].max()

    grid_shape = (
        int((max_y - min_y) / pixel_size) + 1,
        int((max_x - min_x) / pixel_size) + 1
    )
    elevation_grid = np.full(grid_shape, np.nan)

    grid_x = ((points[:, 0] - min_x) / pixel_size).astype(int)
    grid_y = ((max_y - points[:, 1]) / pixel_size).astype(int)

    elevation_grid[grid_y, grid_x] = points[:, 2]

    transform = from_origin(min_x, max_y, pixel_size, pixel_size)

    crs = CRS.from_epsg(2056)

    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=elevation_grid.shape[0],
        width=elevation_grid.shape[1],
        count=1,
        dtype='float32',
        crs=crs,
        transform=transform,
        compress='lzw'
    ) as dst:
        dst.write(elevation_grid, 1)

def process_surface(surface, idx, output_tiff_file, num_points, pixel_size):
    points, faces = surface
    interpolated_points = []

    for face in faces:
        if len(face) == 3:
            interpolated_points.extend(interpolate_triangle(face[0], face[1], face[2], num_points=num_points))
            interpolated_points.extend(face)

    all_points = points + interpolated_points
    create_geotiff(all_points, f"{output_tiff_file[:-4]}_surface_{idx}.tif", pixel_size)

def main(landxml_file, output_tiff_file, num_points, pixel_size):
    surfaces = parse_landxml(landxml_file)
    return surfaces

def open_landxml_file():
    file_path = filedialog.askopenfilename(
        defaultextension=".xml",
        filetypes=[("LandXML files", "*.xml"), ("All files", "*.*")]
    )
    if file_path:
        landxml_entry.delete(0, tk.END)
        landxml_entry.insert(0, file_path)

def run_conversion():
    landxml_file = landxml_entry.get()
    if not landxml_file:
        messagebox.showerror("Error", "Please select a LandXML file.")
        return

    try:
        num_points = int(num_points_entry.get())
        pixel_size = float(pixel_size_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for pixel size and number of points.")
        return

    output_tiff_file = os.path.splitext(landxml_file)[0] + ".tif"

    try:
        # Get surfaces using a separate process
        with multiprocessing.Pool(1) as pool:
            surfaces = pool.apply(main, (landxml_file, output_tiff_file, num_points, pixel_size))

        # Process surfaces using ProcessPoolExecutor
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(process_surface, surface, i, output_tiff_file, num_points, pixel_size)
                       for i, surface in enumerate(surfaces, start=1)]

            for future in futures:
                future.result()  # Wait for all processes to complete

        messagebox.showinfo("Success", "GeoTIFF files created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during conversion:\n{e}")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn', force=True)

    window = tk.Tk()
    window.title("LandXML to GeoTIFF Converter")

    landxml_label = tk.Label(window, text="LandXML File:")
    landxml_label.grid(row=0, column=0, padx=10, pady=10)

    landxml_entry = tk.Entry(window, width=50)
    landxml_entry.grid(row=0, column=1, padx=10, pady=10)

    landxml_button = tk.Button(window, text="Browse", command=open_landxml_file)
    landxml_button.grid(row=0, column=2, padx=10, pady=10)

    pixel_size_label = tk.Label(window, text="Pixel Size:")
    pixel_size_label.grid(row=1, column=0, padx=10, pady=10)

    pixel_size_entry = tk.Entry(window, width=20)
    pixel_size_entry.grid(row=1, column=1, padx=10, pady=10)

    num_points_label = tk.Label(window, text="Number of Points:")
    num_points_label.grid(row=2, column=0, padx=10, pady=10)

    num_points_entry = tk.Entry(window, width=20)
    num_points_entry.grid(row=2, column=1, padx=10, pady=10)

    convert_button = tk.Button(window, text="Convert to GeoTIFF", command=run_conversion)
    convert_button.grid(row=3, column=0, columnspan=3, padx=10, pady=20)

    window.mainloop()

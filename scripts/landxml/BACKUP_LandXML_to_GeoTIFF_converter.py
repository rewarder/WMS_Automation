import xml.etree.ElementTree as ET
import numpy as np  
import rasterio
from rasterio.transform import from_origin
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time
import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

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

def create_geotiff(points, output_path, pixel_size=0.15):
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

def process_surface(surface, idx, output_tiff_file):
    points, faces = surface
    interpolated_points = []

    for face in faces:
        if len(face) == 3:
            interpolated_points.extend(interpolate_triangle(face[0], face[1], face[2], num_points=150))
            interpolated_points.extend(face)

    all_points = points + interpolated_points
    create_geotiff(all_points, f"{output_tiff_file[:-4]}_surface_{idx}.tif")

def convert_files():
    landxml_file = entry_filepath.get()
    pixel_size = float(entry_pixel_size.get())
    num_points = int(entry_num_points.get()) # Make sure to get the value from the GUI

    if not landxml_file:
        messagebox.showerror("Error", "Please provide a LandXML file path.")
        return

    start_time = time.time()
    surfaces = parse_landxml(landxml_file)
    
    output_tiff_file = landxml_file.rsplit('.', 1)[0] + '.tif' 

    for i, surface in enumerate(surfaces, start=1):
        process_surface(surface, i, output_tiff_file) # Pass num_points here

    end_time = time.time()
    execution_time = end_time - start_time
    with open('execution_time_no_threads.txt', 'w') as f:
        f.write(f"Total execution time: {execution_time:.2f} seconds\n")
    messagebox.showinfo("Success", f"Conversion completed! GeoTIFF files saved.")

def drop(event):
    filepath = event.data
    entry_filepath.delete(0, tk.END)
    entry_filepath.insert(0, filepath)

# Set up the GUI
root = TkinterDnD.Tk()
root.title("LandXML to GeoTIFF Converter")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# File Path Entry
ttk.Label(frame, text="Drag and drop LandXML file:").grid(column=0, row=0, sticky=tk.W)
entry_filepath = ttk.Entry(frame, width=50)
entry_filepath.grid(column=0, row=1, sticky=(tk.W, tk.E))
entry_filepath.drop_target_register(DND_FILES)
entry_filepath.dnd_bind('<<Drop>>', drop)

# Pixel Size Entry
ttk.Label(frame, text="Pixel Size:").grid(column=0, row=2, sticky=tk.W)
entry_pixel_size = ttk.Entry(frame)
entry_pixel_size.grid(column=0, row=3, sticky=(tk.W, tk.E))
entry_pixel_size.insert(0, '0.15')  # Default value

# Number of Points Entry
ttk.Label(frame, text="Number of Points:").grid(column=0, row=4, sticky=tk.W)
entry_num_points = ttk.Entry(frame)
entry_num_points.grid(column=0, row=5, sticky=(tk.W, tk.E))
entry_num_points.insert(0, '150')  # Default value

# Convert Button
btn_convert = ttk.Button(frame, text="Convert", command=convert_files)
btn_convert.grid(column=0, row=6, pady=10)

root.mainloop()

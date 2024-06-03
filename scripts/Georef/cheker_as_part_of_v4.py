import ezdxf
import os
import sys
import shutil
import datetime
import time

# Import all the required functions
from explode_blocks import explode_blocks
from explode_dimensions import explode_dimensions
from explode_mtext import explode_mtext
from create_hatch_boundaries import create_hatch_boundary_for_all_hatches
from text_2_lines import extract_text_and_positions, text_to_boundary_lines, polylines_to_lines
from delete_entities import delete_hatch_entities, delete_point_entities, delete_text_entities, delete_mtext_entities, delete_body_entities, delete_image_entities, delete_wipeout_entities, delete_solid_entities, delete_3dsolid_entities
from entity_counter import count_entities

# Georeferencing functions from georef_checker.py
def is_within_bounds(entity, min_x, min_y, max_x, max_y):
    """Check if an entity is within the given bounds."""
    if entity.dxftype() == 'LINE':
        return (min_x <= entity.dxf.start.x <= max_x and min_y <= entity.dxf.start.y <= max_y) or \
               (min_x <= entity.dxf.end.x <= max_x and min_y <= entity.dxf.end.y <= max_y)
    elif entity.dxftype() == 'LWPOLYLINE':
        return any(min_x <= x <= max_x and min_y <= y <= max_y for x, y in entity.get_points(format='xy'))
    elif entity.dxftype() == 'CIRCLE':
        center = entity.dxf.center
        radius = entity.dxf.radius
        return (min_x <= center.x - radius <= max_x and min_y <= center.y - radius <= max_y) and \
               (min_x <= center.x + radius <= max_x and min_y <= center.y + radius <= max_y)
    else:
        return False  # Add conditions for other entity types as needed

def find_entities_within_bounds(dxf_path, min_x, min_y, max_x, max_y):
    """Find all entities within the given bounds in a DXF file."""
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    return [entity for entity in msp if is_within_bounds(entity, min_x, min_y, max_x, max_y)]

def is_georeferenced(dxf_path, min_x, min_y, max_x, max_y):
    """Check if the DXF file is georeferenced by finding entities within bounds."""
    entities = find_entities_within_bounds(dxf_path, min_x, min_y, max_x, max_y)
    return len(entities) > 0

# Define the boundary coordinates (bottom-left and top-right)
min_x, min_y = 2400000, 1100000  # Bottom-left coordinates
max_x, max_y = 2900000, 1300000  # Top-right coordinates

# Log the different steps
def log_operation(operation_name, status, log_file_path, error_msg=None, extra_info="No extra info"):
    with open(log_file_path, 'a') as log_file:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {operation_name} - {status}"
        if error_msg:
            log_entry += f" - Error: {error_msg}"
        log_entry += f" - Info: {extra_info}\n"
        log_file.write(log_entry)

# Main function to process the dxf input file 
def process_dxf(input_file, output_file, log_file_path):
    # Check if the DXF file is georeferenced
    if not is_georeferenced(input_file, min_x, min_y, max_x, max_y):
        log_operation("Georeference Check", "Failed", log_file_path, error_msg="The plan is not georeferenced.")
        print("The plan you uploaded has not been georeferenced. Please upload a georeferenced plan.")
        return

    # Proceed with processing if georeferenced
    log_operation("Georeference Check", "Passed", log_file_path, extra_info="The plan is georeferenced.")
    print("The plan is georeferenced. Proceeding with the main program.")
    
    # Add your main processing steps here
    # Example: Call other functions to process the DXF file
    try:
        explode_blocks(input_file, output_file)
        log_operation("Explode Blocks", "
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
from splines_2_lines import splines_2_lines
from create_hatch_boundaries import create_hatch_boundary_for_all_hatches
from render_shp_font_kerning import convert_text_in_dxf
from polylines_to_lines import polylines_to_lines
from polyline_2d_2_lines import convert_2d_polylines_to_lines
from polyline_3d_2_lines import convert_3d_polylines_to_lines
from ellipse_to_lines import redraw_ellipses
from face3d_boundary_lines import create_face3d_boundary_lines
from delete_entities import delete_leader_entities, delete_face3D_entities, delete_mpolygon_entities, delete_polyline_entities, delete_hatch_entities, delete_point_entities, delete_text_entities, delete_mtext_entities, delete_body_entities, delete_image_entities, delete_wipeout_entities, delete_solid_entities, delete_3dsolid_entities
from delete_identical_lines import find_and_delete_identical_lines
from entity_counter import count_entities
from layer_rename import rename_layers_in_memory
from purge import purge_dxf
from georef_outside_ch_entity_delete import delete_entities_outside_boundary
from delete_layers_set_to_off import delete_off_layers_and_entities
from flatten_lines import flatten3d_lines

"""# Check if entities are within bounding box (approximately Switzerland)
def is_within_bounds(entity, min_x, min_y, max_x, max_y):
    # Check if an entity is within the given bounds.
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

# Return entities that are within boundary
def find_entities_within_bounds(dxf_path, min_x, min_y, max_x, max_y):
    # Find all entities within the given bounds in a DXF file.
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    return [entity for entity in msp if is_within_bounds(entity, min_x, min_y, max_x, max_y)]

# Perform the actual check
def is_georeferenced(dxf_path, min_x, min_y, max_x, max_y):
    # Check if the DXF file is georeferenced by finding entities within bounds.
    entities = find_entities_within_bounds(dxf_path, min_x, min_y, max_x, max_y)
    return len(entities) > 0

# Define the boundary coordinates (bottom-left and top-right), aka approximate Switzerland with a rectangle
min_x, min_y = 2400000, 1100000  # Bottom-left coordinates
max_x, max_y = 2900000, 1300000  # Top-right coordinates"""

# Log the different steps
def log_operation(operation_name, status, log_file_path, error_msg=None, extra_info="No extra info"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S") # Add a time stamp
    if status:
        log_entry = f"{timestamp} - {operation_name} - {extra_info}: SUCCESS\n" # Build a log entry with time stamp, name of the operation and extra info, which is used for the timer
    else:
        log_entry = f"{timestamp} - {operation_name} - {extra_info}: FAILURE - {error_msg}\n" # Build a log entry in the case of error, by adding the error message
    with open(log_file_path, 'a') as log_file: # write the log file
        log_file.write(log_entry)

""" 
Main function to process the dxf input file 
The function accepts/reads an input file in .dxf file format and executes the following operations: 
- Check if the the input file is georeference or not, if georeferenced proceed, if not abort
- Deleting deactivated layers and associated entities
- Bursting by copying all entities within a block and adding them to the map space 
- Extract text, positions, heights, and rotations
- Convert text to boundary lines within the same drawing
- Convert polylines to lines within the same document
- Create boundary lines for all hatches
- Delete all hatch entities
- Delete all text entities
- Delete all MText entities
- Delete all point entities
- Delete all body entities
- Delete all iamge entities
- Delete all wipeout entities
- Delete all solid entities
- Delete all 3Dsolid entities
- Cleanup intermediate files created during the previous operations
- Count all entities
"""
def process_dxf(input_file, output_file, log_file_path):
    start_time = time.time()  # Record the start time

    # Check if the DXF file is georeferenced
    """if not is_georeferenced(input_file, min_x, min_y, max_x, max_y):
        log_operation("Georeference Check", False, log_file_path, error_msg="The plan is not georeferenced.")
        print("The plan you uploaded has not been georeferenced. Please upload a georeferenced plan.")
        return"""

    # Proceed with processing if georeferenced
    log_operation("Georeference Check", True, log_file_path, extra_info="The plan is georeferenced.")
    print("The plan is georeferenced. Proceeding with the main program.")

    # We'll use the same directory as the input file for intermediate files
    base_dir = os.path.dirname(input_file)
    
    # Create a list to store the names of the intermediate files
    intermediate_files = [
        os.path.join(base_dir, f"intermediate_file{i}.dxf") for i in range(1, 7)
    ]

    current_file = input_file

    # Step 1: Delete off layers and entities
    try:
        delete_off_layers_and_entities(current_file, intermediate_files[0])
        log_operation("Off layers and entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_off_layers_and_entities operation failed", False, log_file_path, str(e))
        raise e

    current_file = intermediate_files[0]

    # Step 2: Explode dimensions
    try:
        explode_dimensions(current_file, intermediate_files[1])
        log_operation("Dimensions have been exploded", True, log_file_path)
    except Exception as e:
        log_operation("explode_dimensions operation failed", False, log_file_path, str(e))
        raise e

    current_file = intermediate_files[1]

    # Step 3: Explode blocks
    try:
        explode_blocks(current_file, intermediate_files[2])
        log_operation("Blocks have been exploded", True, log_file_path)
    except Exception as e:
        log_operation("explode_block operation failed", False, log_file_path, str(e))
        raise e

    current_file = intermediate_files[2]

    # Step 4: Explode MText
    try:
        explode_mtext(current_file, intermediate_files[3])
        log_operation("MText has been exploded", True, log_file_path)
    except Exception as e:
        log_operation("explode_mtext operation failed", False, log_file_path, str(e))
        raise e
    
    current_file = intermediate_files[3]
    
    # Load the intermediate file
    doc = ezdxf.readfile(current_file)
    
    # Step 5: Purge unused elements
    """try: 
        # Call the purge function
        purge_dxf(doc) # Purge unused elements
        log_operation("Elements have been purged", True, log_file_path)
    except Exception as e:
        log_operation("Something went wrong while purging elements", False, log_file_path, str(e))
        raise e"""
    
    # Step 6: Convert text to lines based on isocp.shx font
    try:
        convert_text_in_dxf(doc)
        log_operation("Text boundary lines have been created", True, log_file_path)
    except Exception as e:
        log_operation("text_to_boundary_lines", False, log_file_path, str(e))
        raise e

    # Step 7: Convert polylines to lines within the same document
    try:
        polylines_to_lines(doc)
        log_operation("Polylines have been converted to lines", True, log_file_path)
    except Exception as e:
        log_operation("polylines_to_lines", False, log_file_path, str(e))
        raise e

    # Step 8: Convert ellipses to lines within the same document

    try:
        redraw_ellipses(doc)
        log_operation("Ellipses have been redrawn", True, log_file_path)
    except Exception as e: 
        log_operation("redraw_ellipse", False, log_file_path, str(e))

    # Step 9: Convert splines to lines via polylines within the same document
    try:
        splines_2_lines(doc)
        log_operation("Splines have been converted to lines", True, log_file_path)
    except Exception as e:
        log_operation("splines_2_polylines", False, log_file_path, str(e))
        raise e

    # Step 10: Convert 2D Polylines to lines
    try:
        convert_2d_polylines_to_lines(doc)
        log_operation("2D Polylines have been converted to lines", True, log_file_path)
    except Exception as e:
        log_operation("convert_2d_polylines_to_lines", False, log_file_path, str(e))
        raise e

    # Step 11: Convert 3D Polylines to lines
    try:
        convert_3d_polylines_to_lines(doc)
        log_operation("3D Polylines have been converted to lines", True, log_file_path)
    except Exception as e:
        log_operation("convert_3d_polylines_to_lines", False, log_file_path, str(e))
        raise e

    # Step 12: Create boundary lines for all hatches
    try:
        create_hatch_boundary_for_all_hatches(doc)
        log_operation("Boundary lines have been created for all hatches", True, log_file_path)
    except Exception as e:
        log_operation("create_hatch_boundary_for_all_hatches", False, log_file_path, str(e))
        raise e

    # Step 13: Create boundary lines for all Face3D entities
    try:
        create_face3d_boundary_lines(doc)
        log_operation("3DFace boundary lines have been created", True, log_file_path)
    except Exception as e:
        log_operation("create_face3d_boundary_lines", False, log_file_path, str(e))
        raise e

    # Step 14: Rename layers
    try: 
        # Call the rename layers function
        rename_layers_in_memory(doc) # Rename layers according to WMS naming convention
        log_operation("Layers have been renamed according to WMS naming convention", True, log_file_path)
    except Exception as e:
        log_operation("Something went wrong while renaming layers", False, log_file_path, str(e))
        raise e
    
    """# Step 15: Delete all entities outside CH boundary box
    try:
        delete_entities_outside_boundary(doc)
        log_operation("Entities outside CH have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_entities_outside_boundary", False, log_file_path, str(e))
        raise e"""

    # Step 16: Delete identical lines
    try:
        find_and_delete_identical_lines(doc)
        log_operation("Identical lines have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("find_and_delete_identical_lines", False, log_file_path, str(e))
        raise e

    # Step 17: Delete all leader entities
    try:
        delete_leader_entities(doc)
        log_operation("Leader entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_leader_entities", False, log_file_path, str(e))
        raise e

    # Step 18: Delete all Face3D entities
    try:
        delete_face3D_entities(doc)
        log_operation("3DFace entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_face3D_entities", False, log_file_path, str(e))
        raise e

    # Step 19: Delete all MPolygon entities
    try:
        delete_mpolygon_entities(doc)
        log_operation("MPolygon entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_mpolygon_entities", False, log_file_path, str(e))
        raise e  

    # Step 20: Delete all polyline entities
    try:
        delete_polyline_entities(doc)
        log_operation("Polyline entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_polyline_entities", False, log_file_path, str(e))
        raise e

    # Step 21: Delete all hatch entities
    try:
        delete_hatch_entities(doc)
        log_operation("Hatch entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_hatch_entities", False, log_file_path, str(e))
        raise e

    # Step 22: Delete all text entities
    try:
        delete_text_entities(doc)
        log_operation("Text entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_text_entities", False, log_file_path, str(e))
        raise e

    # Step 23: Delete all MText entities
    try:
        delete_mtext_entities(doc)
        log_operation("MText entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_mtext_entities", False, log_file_path, str(e))
        raise e

    # Step 24: Delete all point entities
    try:
        delete_point_entities(doc)
        log_operation("Point entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_point_entities", False, log_file_path, str(e))
        raise e

    # Step 25: Delete all body entities
    try:
        delete_body_entities(doc)
        log_operation("Body entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_body_entities", False, log_file_path, str(e))
        raise e

    # Step 26: Delete all iamge entities
    try:
        delete_image_entities(doc)
        log_operation("Image entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_image_entities", False, log_file_path, str(e))
        raise e

    # Step 27: Delete all wipeout entities
    try:
        delete_wipeout_entities(doc)
        log_operation("Wipeout entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_wipeout_entities", False, log_file_path, str(e))
        raise e

    # Step 28: Delete all solid entities
    try:
        delete_solid_entities(doc)
        log_operation("Solid entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_solid_entities", False, log_file_path, str(e))
        raise e

    # Step 29: Delete all 3Dsolid entities
    try:
        delete_3dsolid_entities(doc)
        log_operation("3DSolid entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_3dsolid_entities", False, log_file_path, str(e))
        raise e

    # Step 30: Flatten all lines
    try:
        flatten3d_lines(doc)
        log_operation("Line entities have been flattened", True, log_file_path)
    except Exception as e:
        log_operation("flatten3d_lines", False, log_file_path, str(e))
        raise e
    
    # Step 5: Purge unused elements
    """try: 
        # Call the purge function again
        purge_dxf(doc) # Purge unused elements
        log_operation("Elements have been purged again", True, log_file_path)
    except Exception as e:
        log_operation("Something went wrong while purging elements again", False, log_file_path, str(e))
        raise e"""

    # Step 31: Save the current state to a file and then re-open it for explode_blocks
    doc.saveas(output_file)

    # Step 32: Cleanup intermediate files
    for file in intermediate_files:
        try:
            if os.path.exists(file):
                os.remove(file)
            log_operation(f"cleanup {file}", True, log_file_path)
        except Exception as e:
            log_operation(f"cleanup {file}", False, log_file_path, str(e))
            # Handle the error if necessary

    # Step 33: It's time to count all entities
    try:
        doc = ezdxf.readfile(output_file)
        entity_count = count_entities(doc)
        log_operation("Entity Count", True, log_file_path)

        for dxf_type, count in entity_count.items():
            log_operation(f"{dxf_type}: {count}", True, log_file_path)

    except Exception as e:
        log_operation("Something went wrong while counting the entities", False, log_file_path, str(e))
        raise e

    # At the end of the process, before the final log entry
    end_time = time.time() # Record the end time
    total_time = end_time - start_time # Calculate the total time taken

    # Log the total execution time
    log_operation("Total Execution Time ", True, log_file_path, extra_info=f"{total_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: drag and drop a DXF file onto this script.")
        sys.exit(1)
    
    # Files can be processed by dragging the input file onto the an exe, which is compiled using pyinstaller --onefile --windowed
    input_file_path = sys.argv[1]
    input_dir, input_filename = os.path.split(input_file_path)
    output_file_name = f"modified_{input_filename}"
    output_file_path = os.path.join(input_dir, output_file_name)

    # Define log file path
    log_file_name = f"log_{input_filename.replace('.dxf', '')}.txt"
    log_file_path = os.path.join(input_dir, log_file_name)

    try:
        process_dxf(input_file_path, output_file_path, log_file_path)
        print(f"DXF file successfully processed and saved to: {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        log_operation("Script Execution", False, log_file_path, str(e))  # Log the exception

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
from text_2_lines import extract_text_and_positions, text_to_boundary_lines, polylines_to_lines
from delete_entities import delete_hatch_entities, delete_point_entities, delete_text_entities, delete_mtext_entities, delete_body_entities, delete_image_entities, delete_wipeout_entities, delete_solid_entities, delete_3dsolid_entities
from entity_counter import count_entities
from layer_rename import rename_layers

# Check if entities are within bounding box (approximately Switzerland)
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
max_x, max_y = 2900000, 1300000  # Top-right coordinates

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
- Bursting blocks 5 times in a row by copying all entities within a block and adding them to the map space 
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
- Save the current state to a file and then re-open it for explode_blocks
- Explode blocks one last time
- Cleanup intermediate files created during the previous operations
- Count all entities
"""
def process_dxf(input_file, output_file, log_file_path):
    start_time = time.time() # Record the start time

    # Check if the DXF file is georeferenced
    if not is_georeferenced(input_file, min_x, min_y, max_x, max_y):
        log_operation("Georeference Check", False, log_file_path, error_msg="The plan is not georeferenced.")
        print("The plan you uploaded has not been georeferenced. Please upload a georeferenced plan.")
        return

    # Proceed with processing if georeferenced
    log_operation("Georeference Check", True, log_file_path, extra_info="The plan is georeferenced.")
    print("The plan is georeferenced. Proceeding with the main program.")

    # We'll use the same directory as the input file for intermediate files
    base_dir = os.path.dirname(input_file)
    
    # Create a list to store the names of the intermediate files
    intermediate_files = [
        os.path.join(base_dir, f"intermediate_file{i}.dxf") for i in range(1, 7)
    ]

    # Now, we'll explode blocks 5 times in a row
    current_file = input_file
    for i in range(5):
        try:
            explode_blocks(current_file, intermediate_files[i])
            log_operation(f"Blocks have been exploded {i+1}", True, log_file_path)
        except Exception as e:
            log_operation(f"explode_blocks iteration {i+1}", False, log_file_path, str(e))
            raise e
        
        current_file = intermediate_files[i]
    
    try:
        # The last exploded file will be passed to the next function
        explode_dimensions(current_file, intermediate_files[5])
        log_operation("Dimensions have been exploded", True, log_file_path)
    except Exception as e:
        log_operation("explode_dimensions", False, log_file_path, str(e))
        raise e
        
    current_file = intermediate_files[5]

    # Continue with the rest of the process
    try:
        explode_mtext(current_file, intermediate_files[5])
        log_operation("MText has been exploded", True, log_file_path)
    except Exception as e:
        log_operation("explode_mtext", False, log_file_path, str(e))
        raise e
    
    # Extract text, positions, heights, and rotations
    try:
        extracted_text, positions, heights, rotations = extract_text_and_positions(current_file)
        log_operation("Text, positions, heights and rotation angles have been extracted", True, log_file_path)
    except Exception as e:
        log_operation("extract_text_and_positions", False, log_file_path, str(e))
        raise e
    
    # Load the intermediate file
    doc = ezdxf.readfile(current_file)
    
    # Convert text to boundary lines within the same drawing
    try:
        doc = text_to_boundary_lines(extracted_text, positions, heights, rotations, doc)
        log_operation("Text boundary lines have been created", True, log_file_path)
    except Exception as e:
        log_operation("text_to_boundary_lines", False, log_file_path, str(e))
        raise e

    # Convert polylines to lines within the same document
    try:
        polylines_to_lines(doc)
        log_operation("Polylines have been converted to lines", True, log_file_path)
    except Exception as e:
        log_operation("polylines_to_lines", False, log_file_path, str(e))
        raise e

    # Convert splines to lines via polylines within the same document
    try:
        splines_2_lines(doc)
        log_operation("Splines have been converted to lines", True, log_file_path)
    except Exception as e:
        log_operation("splines_2_polylines", False, log_file_path, str(e))
        raise e

    # Create boundary lines for all hatches
    try:
        create_hatch_boundary_for_all_hatches(doc)
        log_operation("Boundary lines have been created for all hatches", True, log_file_path)
    except Exception as e:
        log_operation("create_hatch_boundary_for_all_hatches", False, log_file_path, str(e))
        raise e

    # Delete all hatch entities
    try:
        delete_hatch_entities(doc)
        log_operation("Hatch entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_hatch_entities", False, log_file_path, str(e))
        raise e

    # Delete all text entities
    try:
        delete_text_entities(doc)
        log_operation("Text entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_text_entities", False, log_file_path, str(e))
        raise e

    # Delete all MText entities
    try:
        delete_mtext_entities(doc)
        log_operation("MText entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_mtext_entities", False, log_file_path, str(e))
        raise e

    # Delete all point entities
    try:
        delete_point_entities(doc)
        log_operation("Point entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_point_entities", False, log_file_path, str(e))
        raise e

    # Delete all body entities
    try:
        delete_body_entities(doc)
        log_operation("Body entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_body_entities", False, log_file_path, str(e))
        raise e

    # Delete all iamge entities
    try:
        delete_image_entities(doc)
        log_operation("Image entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_image_entities", False, log_file_path, str(e))
        raise e

    # Delete all wipeout entities
    try:
        delete_wipeout_entities(doc)
        log_operation("Wipeout entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_wipeout_entities", False, log_file_path, str(e))
        raise e

    # Delete all solid entities
    try:
        delete_solid_entities(doc)
        log_operation("Solid entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_solid_entities", False, log_file_path, str(e))
        raise e

    # Delete all 3Dsolid entities
    try:
        delete_3dsolid_entities(doc)
        log_operation("3DSolid entities have been deleted", True, log_file_path)
    except Exception as e:
        log_operation("delete_3dsolid_entities", False, log_file_path, str(e))
        raise e

    # Rename layers
    try: 
        # Call the rename layers function
        rename_layers(doc) # Rename layers according to WMS naming convention
        log_operation("Layers have been renamed according to WMS naming convention", True, log_file_path)
    except Exception as e:
        log_operation("Something went wrong while renaming layers", False, log_file_path, str(e))
        raise e

    # Save the current state to a file and then re-open it for explode_blocks
    doc.saveas(output_file)

    # Now call explode_blocks once more on the output file
    try:
        explode_blocks(output_file, output_file)  # Exploding blocks again on the final output file
        log_operation("Block have been exploded one more time", True, log_file_path)
    except Exception as e:
        log_operation("final explode_blocks", False, log_file_path, str(e))
        raise e

    # Cleanup intermediate files
    for file in intermediate_files:
        try:
            if os.path.exists(file):
                os.remove(file)
            log_operation(f"cleanup {file}", True, log_file_path)
        except Exception as e:
            log_operation(f"cleanup {file}", False, log_file_path, str(e))
            # Handle the error if necessary

    # It's time to count all entities
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

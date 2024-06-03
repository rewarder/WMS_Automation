import ezdxf
import os
import sys
import shutil

# Assuming that the following imports are modules with functions you need
from explode_blocks import explode_blocks
from explode_dimensions import explode_dimensions
from explode_mtext import explode_mtext
from create_hatch_boundaries import create_hatch_boundary_for_all_hatches
from delete_hatches import delete_hatches
from text_2_lines import extract_text_and_positions, text_to_boundary_lines, polylines_to_lines
from delete_text import delete_all_text_entities
from delete_points import delete_all_point_entities
from delete_entities import delete_hatch_entities, delete_point_entities, delete_text_entities, delete_mtext_entities, delete_body_entities, delete_image_entities, delete_wipeout_entities, delete_solid_entities, delete_3dsolid_entities

def process_dxf(input_file, output_file):
    # We'll use the same directory as the input file for intermediate files
    base_dir = os.path.dirname(input_file)
    
    # Create a list to store the names of the intermediate files
    intermediate_files = [
        os.path.join(base_dir, f"intermediate_file{i}.dxf") for i in range(1, 7)
    ]

    # Now, we'll explode blocks 5 times in a row
    current_file = input_file
    for i in range(5):
        explode_blocks(current_file, intermediate_files[i])
        current_file = intermediate_files[i]
    
    # The last exploded file will be passed to the next function
    explode_dimensions(current_file, intermediate_files[5])
    current_file = intermediate_files[5]

    # Continue with the rest of the process
    explode_mtext(current_file, intermediate_files[5])
    
    # Extract text, positions, heights, and rotations
    extracted_text, positions, heights, rotations = extract_text_and_positions(current_file)
    
    # Load the intermediate file
    doc = ezdxf.readfile(current_file)
    
    # Convert text to boundary lines within the same drawing
    doc = text_to_boundary_lines(extracted_text, positions, heights, rotations, doc)
    
    # Convert polylines to lines within the same document
    polylines_to_lines(doc)
    
    create_hatch_boundary_for_all_hatches(doc)
    delete_hatch_entities(doc)

    # Delete all text entities
    delete_text_entities(doc)

    # Delete all MText entities
    delete_mtext_entities(doc)

    # Delete all point entities
    delete_point_entities(doc)

    # Delete all body entities
    delete_body_entities(doc)

    # Delete all iamge entities
    delete_image_entities(doc)

    # Delete all wipeout entities
    delete_wipeout_entities(doc)

    # Delete all solid entities
    delete_solid_entities(doc)

    # Delete all 3Dsolid entities
    delete_3dsolid_entities(doc) 

    # Save the current state to a file and then re-open it for explode_blocks
    doc.saveas(output_file)

    # Now call explode_blocks once more on the output file
    explode_blocks(output_file, output_file)  # Exploding blocks again on the final output file

    # Cleanup intermediate files
    for file in intermediate_files:
        if os.path.exists(file):
            os.remove(file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: drag and drop a DXF file onto this script.")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    input_dir, input_filename = os.path.split(input_file_path)
    output_file_name = f"modified_{input_filename}"
    output_file_path = os.path.join(input_dir, output_file_name)

    process_dxf(input_file_path, output_file_path)

    print(f"DXF file successfully processed and saved to: {output_file_path}")

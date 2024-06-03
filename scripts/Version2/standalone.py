import ezdxf
import os
import sys
import shutil

from explode_blocks import explode_blocks
from explode_dimensions import explode_dimensions
from explode_mtext import explode_mtext
from create_hatch_boundaries import create_hatch_boundary_for_all_hatches
from delete_hatches import delete_hatches
from text_2_lines import extract_text_and_positions, text_to_boundary_lines, polylines_to_lines
from delete_text import delete_all_text_entities
from delete_points import delete_all_point_entities

def process_dxf(input_file, output_file):
    # We'll use the same directory as the input file for intermediate files
    base_dir = os.path.dirname(input_file)
    intermediate_file1 = os.path.join(base_dir, "intermediate_file1.dxf")
    intermediate_file2 = os.path.join(base_dir, "intermediate_file2.dxf")
    intermediate_file3 = os.path.join(base_dir, "intermediate_file3.dxf")
    intermediate_file_before_final = os.path.join(base_dir, "intermediate_file_before_final.dxf")

    # Execute scripts one by one on corresponding intermediate files
    explode_blocks(input_file, intermediate_file1)
    explode_dimensions(intermediate_file1, intermediate_file2)
    explode_mtext(intermediate_file2, intermediate_file3)
    
    # Extract text, positions, heights and rotations
    extracted_text, positions, heights, rotations = extract_text_and_positions(intermediate_file3)
    
    # Load the intermediate file 3
    doc = ezdxf.readfile(intermediate_file3)
    
    # Convert text to boundary lines within the same drawing
    doc = text_to_boundary_lines(extracted_text, positions, heights, rotations, doc)
    
    # Convert polylines to lines within the same document
    polylines_to_lines(doc)
    
    create_hatch_boundary_for_all_hatches(doc)
    delete_hatches(doc)

    # Delete all text entities
    delete_all_text_entities(doc)

    # Delete all point entities
    delete_all_point_entities(doc)

    # Save the current state to a file and then re-open it for explode_blocks
    doc.saveas(intermediate_file_before_final)
    explode_blocks(intermediate_file_before_final, output_file)

    # Cleanup intermediate files
    os.remove(intermediate_file1)
    os.remove(intermediate_file2)
    os.remove(intermediate_file3)
    os.remove(intermediate_file_before_final)


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

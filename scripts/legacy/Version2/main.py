import ezdxf
from explode_blocks import explode_blocks
from explode_dimensions import explode_dimensions
from explode_mtext import explode_mtext
from create_hatch_boundaries import create_hatch_boundary_for_all_hatches
from delete_hatches import delete_hatches
from text_2_lines import extract_text_and_positions, text_to_boundary_lines, polylines_to_lines
from delete_text import delete_all_text_entities
from delete_points import delete_all_point_entities

if __name__ == "__main__":
    # Define the input file path and intermediate paths
    input_file = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/ExplodeAndConvert/input.dxf"
    intermediate_file1 = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/ExplodeAndConvert/intermediate_file1.dxf"
    intermediate_file2 = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/ExplodeAndConvert/intermediate_file2.dxf"
    intermediate_file3 = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/ExplodeAndConvert/intermediate_file3.dxf"
    intermediate_file4 = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/ExplodeAndConvert/intermediate_file4.dxf"
    output_file = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/ExplodeAndConvert/output.dxf"

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

    # Call the function to delete all text entities
    delete_all_text_entities(doc)

    # Call the function to delete all point entities
    delete_all_point_entities(doc)

    # Call explode_blocks a second time on the current document before saving
    # We need to save the current state to a file and then re-open it 
    # because explode_blocks expects a file path as input
    intermediate_file_before_final = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/ExplodeAndConvert/intermediate_file_before_final.dxf"
    doc.saveas(intermediate_file_before_final)
    explode_blocks(intermediate_file_before_final, output_file)
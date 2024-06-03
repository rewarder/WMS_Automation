import ezdxf

def delete_all_body_entities(dxf_file_path, save_to=None):
    """
    Deletes all 'BODY' entities in the given DXF file.

    Args:
    - dxf_file_path: The path to the DXF file to be processed.
    - save_to: The path where the modified DXF file should be saved. If None, it will overwrite the original file.
    """

    # Load the DXF document
    doc = ezdxf.readfile(dxf_file_path)

    # We will modify the modelspace as this is where 'BODY' entities typically reside
    modelspace = doc.modelspace()

    # Find and delete all 'BODY' entities
    bodies_to_delete = [entity for entity in modelspace if entity.dxftype() == 'BODY']
    for body in bodies_to_delete:
        modelspace.delete_entity(body)

    # Save the modified document
    if save_to is None:
        save_to = dxf_file_path
    doc.saveas(save_to)
    print(f"All 'BODY' entities have been deleted. File saved as: {save_to}")

# Example usage:
# Provide the path to your DXF file here and call the function
input_dxf_path = 'path_to_your_dxf_file.dxf'
output_dxf_path = 'path_to_save_modified_dxf_file.dxf'  # Optional, use None to overwrite
delete_all_body_entities(input_dxf_path, output_dxf_path)

import ezdxf

def delete_wipeout_entities(dxf_file_path, output_file_path=None):
    # Load the DXF document
    doc = ezdxf.readfile(dxf_file_path)
    
    # If no output path is provided, overwrite the input file
    if output_file_path is None:
        output_file_path = dxf_file_path

    # Iterate through modelspace and remove wipeout entities
    msp = doc.modelspace()
    wipeouts = msp.query('WIPEOUT')
    for wipeout in wipeouts:
        msp.delete_entity(wipeout)

    # Save the modified DXF document
    doc.saveas(output_file_path)
    print(f"All WIPEOUT entities have been removed from {dxf_file_path}.")

# Example usage:
delete_wipeout_entities('your_input_file.dxf', 'your_output_file.dxf')

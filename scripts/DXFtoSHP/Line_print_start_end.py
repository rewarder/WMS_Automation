import ezdxf

def print_line_coordinates(dxf_file_path):
    # Load the DXF document
    doc = ezdxf.readfile(dxf_file_path)
    msp = doc.modelspace()

    # Iterate through all entities in the model space
    for entity in msp:
        # Check if the entity is a LINE
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            print(f"Start: {start}, End: {end}")

if __name__ == "__main__":
    # Specify the path to your DXF file
    input_dxf_file = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/DXFtoSHP/some_more_multiple_Lines.dxf"
    
    # Call the function with the path to your DXF file
    print_line_coordinates(input_dxf_file)

import ezdxf

def is_2d_polyline(polyline):
    # Check if the polyline is closed
    if not polyline.is_closed:
        return False

    # Check if all vertices have the same z-coordinate (2D polyline)
    z_coords = set(point[2] for point in polyline.points())
    if len(z_coords) == 1:
        return True
    else:
        return False

def convert_2d_polylines_to_lines(input_filename, output_filename):
    # Load the DXF file
    doc = ezdxf.readfile(input_filename)

    # Create a new DXF document for output
    out_doc = ezdxf.new()

    # Create a new modelspace in the output document
    msp = out_doc.modelspace()

    # Iterate through all entities in the modelspace
    for entity in doc.modelspace():
        if entity.dxftype() == 'POLYLINE' and is_2d_polyline(entity):
            # Get the vertices of the 2D polyline
            vertices = list(entity.points())

            # Convert the 2D polyline to lines by connecting consecutive vertices
            for i in range(len(vertices) - 1):
                start_point = vertices[i]
                end_point = vertices[i + 1]
                msp.add_line(start_point, end_point)

    # Save the output DXF file
    out_doc.saveas(output_filename)
    print(f'Conversion completed. Output saved to {output_filename}')

# Specify input and output filenames
input_file = 'C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/SimpleDXFentities/2d_polylines_copy.dxf'
output_file = 'C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/SimpleDXFentities/converted_2d_polylines_copy.dxf'

# Call the conversion function
convert_2d_polylines_to_lines(input_file, output_file)

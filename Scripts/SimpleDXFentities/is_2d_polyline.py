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

def check_2d_polylines(input_filename):
    # Load the DXF file
    doc = ezdxf.readfile(input_filename)

    # Iterate through all entities in the modelspace
    for entity in doc.modelspace():
        if entity.dxftype() == 'POLYLINE':
            if is_2d_polyline(entity):
                print(f'Entity {entity.dxf.handle} is a 2D polyline')
            else:
                print(f'Entity {entity.dxf.handle} is not a 2D polyline')

# Specify input filename
input_file = 'C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/SimpleDXFentities/2d_polylines.dxf'

# Call the function to check 2D polylines
check_2d_polylines(input_file)

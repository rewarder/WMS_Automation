import ezdxf

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

def find_entities_within_bounds(dxf_path, min_x, min_y, max_x, max_y):
    """Find all entities within the given bounds in a DXF file."""
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    return [entity for entity in msp if is_within_bounds(entity, min_x, min_y, max_x, max_y)]

def is_georeferenced(dxf_path, min_x, min_y, max_x, max_y):
    """Check if the DXF file is georeferenced by finding entities within bounds."""
    entities = find_entities_within_bounds(dxf_path, min_x, min_y, max_x, max_y)
    return len(entities) > 0

# Define the boundary coordinates (bottom-left and top-right)
min_x, min_y = 2400000, 1100000  # Bottom-left coordinates
max_x, max_y = 2900000, 1300000  # Top-right coordinates

# Path to the DXF file
dxf_file_path = 'C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Georef/outofboundry.dxf'

# Check if the DXF file is georeferenced
if is_georeferenced(dxf_file_path, min_x, min_y, max_x, max_y):
    # Proceed with the main program
    print("The plan is georeferenced. Proceeding with the main program.")

    # Example: Find entities within the defined boundaries
    entities = find_entities_within_bounds(dxf_file_path, min_x, min_y, max_x, max_y)

    # Do something with the found entities, e.g., print them out
    for entity in entities:
        print(entity)
else:
    # Stop the program and throw a message
    print("The plan you uploaded has not been georeferenced. Please upload a georeferenced plan.")

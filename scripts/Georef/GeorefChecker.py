import ezdxf

def is_within_bounds(entity, min_x, min_y, max_x, max_y):
    if entity.dxftype() == 'LINE':
        # For lines, check both start and end points
        return (min_x <= entity.dxf.start.x <= max_x and min_y <= entity.dxf.start.y <= max_y) or \
               (min_x <= entity.dxf.end.x <= max_x and min_y <= entity.dxf.end.y <= max_y)
    elif entity.dxftype() == 'LWPOLYLINE':
        # For LWPOLYLINES, check each vertex
        for point in entity.get_points(format='xy'):
            x, y = point
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True  # Return True if any vertex is within bounds
        return False
    elif entity.dxftype() == 'CIRCLE':
        # For circles, check if the center plus radius is within bounds
        center = entity.dxf.center
        radius = entity.dxf.radius
        return (min_x <= center.x - radius <= max_x and min_y <= center.y - radius <= max_y) and \
               (min_x <= center.x + radius <= max_x and min_y <= center.y + radius <= max_y)
    else:
        # Add conditions for other entity types as needed
        return False

def find_entities_within_bounds(dxf_path, min_x, min_y, max_x, max_y):
    # Load the DXF file
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()

    # List to hold entities within bounds
    entities_within_bounds = []

    # Iterate over all entities in the model space
    for entity in msp:
        if is_within_bounds(entity, min_x, min_y, max_x, max_y):
            print(f"Entity {entity.dxftype()} within bounds: {entity}")
            entities_within_bounds.append(entity)

    return entities_within_bounds

# Define the boundary coordinates (bottom-left and top-right)
min_x, min_y = 2400000, 1100000  # Bottom-left coordinates
max_x, max_y = 2900000, 1300000  # Top-right coordinates

# Path to the DXF file
dxf_file_path = 'C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Georef/outofboundry.dxf'

# Find entities within the defined boundaries
entities = find_entities_within_bounds(dxf_file_path, min_x, min_y, max_x, max_y)

# Do something with the found entities
# For example, print them out
for entity in entities:
    print(entity)

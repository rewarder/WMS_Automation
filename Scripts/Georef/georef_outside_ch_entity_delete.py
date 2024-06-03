import ezdxf
from ezdxf.math import Vec2

# Define the boundary coordinates for Switzerland in LV95 coordinate system
switzerland_boundary = [
    Vec2(2482899.161, 1074290.533),  # top left corner
    Vec2(2835908.050, 1074290.533),  # top right corner
    Vec2(2835908.050, 1295290.285),  # bottom right corner
    Vec2(2482899.161, 1295290.285)   # bottom left corner
]

def is_inside_switzerland_boundary(point):
    x, y = point
    return (
        x >= switzerland_boundary[0][0] and
        x <= switzerland_boundary[1][0] and
        y >= switzerland_boundary[0][1] and
        y <= switzerland_boundary[2][1]
    )

def process_dxf_document(doc):
    msp = doc.modelspace()

    # Filter out entities that are outside the boundary coordinates for Switzerland
    filtered_entities = [entity for entity in msp if is_inside_switzerland_boundary(entity.dxf.location)]

    # Clear the existing entities in the drawing
    msp.clear()

    # Add the filtered entities back to the drawing
    for entity in filtered_entities:
        msp.add_entity(entity)

    return doc

# Load the input .dxf file
doc = ezdxf.readfile("input.dxf")

# Process the loaded DXF document
modified_doc = process_dxf_document(doc)

# Save the modified drawing to a new .dxf file
modified_doc.saveas("output.dxf")

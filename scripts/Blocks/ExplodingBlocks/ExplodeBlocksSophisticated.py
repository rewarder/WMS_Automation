import ezdxf
from ezdxf.math import Matrix44
import math  # Import the math module for the radians conversion

def explode_block_reference(block_ref, modelspace):
    # Get the block definition
    block_definition = block_ref.block()

    # Get transformation matrix from the block reference
    m = Matrix44.chain(
        Matrix44.translate(block_ref.dxf.insert.x, block_ref.dxf.insert.y, block_ref.dxf.insert.z),
        Matrix44.z_rotate(math.radians(block_ref.dxf.rotation)),  # Convert degrees to radians for rotation
        Matrix44.scale(block_ref.dxf.xscale, block_ref.dxf.yscale, block_ref.dxf.zscale),
    )

    # Copy entities from the block definition and add them to the modelspace
    for entity in block_definition:
        # Don't process entities on frozen or off layers
        if entity.dxf.layer in modelspace.doc.layers and modelspace.doc.layers.get(entity.dxf.layer).is_frozen():
            continue
        if entity.dxf.layer in modelspace.doc.layers and not modelspace.doc.layers.get(entity.dxf.layer).is_on():
            continue

        # Transform and add the entity to the modelspace
        copied_entity = entity.copy()
        if 'AcDbEntity' in copied_entity.dxftype():
            copied_entity.transform(m)
        modelspace.add_entity(copied_entity)

    # Delete the original block reference
    modelspace.delete_entity(block_ref)

# Load the DXF document
doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/input.dxf")

# Access modelspace
modelspace = doc.modelspace()

# Explode all block references
block_refs = list(modelspace.query('INSERT'))  # Use a list to avoid modifying the container during iteration
for block_ref in block_refs:
    explode_block_reference(block_ref, modelspace)

# Save the modified DXF document
doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/exploded_input_file.dxf")
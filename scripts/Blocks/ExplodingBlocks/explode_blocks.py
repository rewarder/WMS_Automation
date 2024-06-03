import ezdxf
from ezdxf.math import Matrix44
import math

def explode_blocks(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    modelspace = doc.modelspace()

    def explode_block_reference(block_ref, modelspace):
        block_definition = block_ref.block()

        """transform_matrix = Matrix44.chain(
            Matrix44.translate(0, 0, 0),
            Matrix44.z_rotate(rotation_radians),
            Matrix44.translate(position[0], position[1], 0)
        )"""

        m = Matrix44.chain(
            Matrix44.translate(block_ref.dxf.insert.x, block_ref.dxf.insert.y, block_ref.dxf.insert.z),
            Matrix44.z_rotate(math.radians(block_ref.dxf.rotation)),
            # Matrix44.scale(block_ref.dxf.xscale, block_ref.dxf.yscale, block_ref.dxf.zscale)
        )
        # Copy entities from the block definition and add them to the modelspace
        for entity in block_definition:
            # Don't process entities on frozen or off layers
            if entity.dxf.layer in modelspace.doc.layers and modelspace.doc.layers.get(entity.dxf.layer).is_frozen():
                continue
            if entity.dxf.layer in modelspace.doc.layers and not modelspace.doc.layers.get(entity.dxf.layer).is_on():
                continue
            
            # Transofrm and add the entity to the modelspace
            copied_entity = entity.copy()
            if 'AcDbEntity' in copied_entity.dxftype():
                copied_entity.transform(m)

        # Preserve all attributes by copying the dxf attributes directly
        copied_entity.dxf.layer = entity.dxf.layer
        copied_entity.dxf.color = entity.dxf.color
        copied_entity.dxf.linetype = entity.dxf.linetype
        copied_entity.dxf.lineweight = entity.dxf.lineweight
        copied_entity.dxf.ltscale = entity.dxf.ltscale
        copied_entity.dxf.invisible = entity.dxf.invisible

        # Access modelspace
        modelspace.add_entity(copied_entity)

        # Delete the original block reference
        modelspace.delete_entity(block_ref)

    # Explode all block references
    block_refs = list(modelspace.query('INSERT')) # Use a list to avoid modifying the container during iteration
    for block_ref in block_refs:
        explode_block_reference(block_ref, modelspace)

    # Save the modified document and pass it on
    doc.saveas(output_file)

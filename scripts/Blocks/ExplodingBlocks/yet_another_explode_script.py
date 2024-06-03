import ezdxf
from ezdxf.math import Matrix44, Vec3

def burst_block_reference(doc, block_ref):
    """
    Explode a block reference (INSERT entity) and convert attributes to text entities.
    """
    msp = doc.modelspace()
    block_name = block_ref.dxf.name
    block = doc.blocks.get(block_name)
    
    # Get the transformation components of the block reference
    insert = block_ref.dxf.insert
    x_scale = block_ref.dxf.xscale
    y_scale = block_ref.dxf.yscale
    z_scale = block_ref.dxf.zscale
    rotation = block_ref.dxf.rotation

    # Construct the transformation matrix
    transform = Matrix44.chain(
        Matrix44.scale(x_scale, y_scale, z_scale),
        Matrix44.z_rotate(rotation),
        Matrix44.translate(insert.x, insert.y, insert.z)
    )

    # Iterate through each entity in the block definition
    for entity in block:
        if entity.dxftype() == 'ATTDEF':
            # Create a text entity for each attribute definition
            attdef = entity
            # Find the corresponding attribute in the block reference
            attr = next((att for att in block_ref.attribs if att.dxf.tag == attdef.dxf.tag), None)
            if attr:
                text_insert = transform.transform(attr.dxf.insert)
                text_rotation = (attr.dxf.rotation + rotation) % 360.0
                msp.add_text(
                    text=attr.dxf.text,
                    dxfattribs={
                        'insert': text_insert,
                        'height': attr.dxf.height,
                        'rotation': text_rotation,
                        'layer': block_ref.dxf.layer,
                        'style': attr.dxf.style,
                        'color': block_ref.dxf.color,
                        'linetype': block_ref.dxf.linetype,
                        'lineweight': block_ref.dxf.lineweight,
                        'ltscale': block_ref.dxf.ltscale,
                    }
                )
        else:
            # Transform and add the entity to model space
            new_entity = entity.copy()
            new_entity.transform(transform)

            # Apply transformation to vertices if the entity has them
            if hasattr(new_entity, 'dxf') and hasattr(new_entity.dxf, 'vertices'):
                new_vertices = [transform.transform(v) for v in new_entity.dxf.vertices]
                new_entity.dxf.vertices = new_vertices

            # Inherit attributes from the block reference
            new_entity.dxf.layer = block_ref.dxf.layer
            new_entity.dxf.color = block_ref.dxf.color
            new_entity.dxf.linetype = block_ref.dxf.linetype
            new_entity.dxf.lineweight = block_ref.dxf.lineweight
            new_entity.dxf.ltscale = block_ref.dxf.ltscale

            msp.add_entity(new_entity)

    # Remove the block reference
    msp.delete_entity(block_ref)

def burst_all_blocks(doc):
    """
    Find all block references (INSERT entities) in the model space and burst them.
    """
    msp = doc.modelspace()
    
    block_references = msp.query('INSERT')
    for block_ref in block_references:
        burst_block_reference(doc, block_ref)

# Load an existing DXF document or create a new one
doc = ezdxf.readfile('C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/another.dxf')

# Burst all blocks in the document
burst_all_blocks(doc)

# Save the modified document
doc.saveas('C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/exploded_another.dxf')

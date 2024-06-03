import ezdxf
from ezdxf.entities import Insert

def explode_blocks(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    msp = doc.modelspace()

    def explode_block_references(msp, block_ref):
        # Get the block definition associated with the block reference
        block_name = block_ref.dxf.name
        block = msp.doc.blocks[block_name]
        # Transform the entities in the block to match the block reference
        for entity in block:
            new_entity = entity.copy()
            # Apply the transformation matrix of the block reference to the new entity
            new_entity.transform(block_ref.matrix44())
            # Inherit attributes from the block reference
            inherit_attributes(new_entity, block_ref)
            msp.add_entity(new_entity)

    def inherit_attributes(entity, block_ref):
        # Inherit common DXF attributes
        entity.dxf.layer = block_ref.dxf.layer
        entity.dxf.color = block_ref.dxf.color
        entity.dxf.linetype = block_ref.dxf.linetype
        entity.dxf.lineweight = block_ref.dxf.lineweight
        entity.dxf.ltscale = block_ref.dxf.ltscale

    # List to store block references for later erasing
    block_refs_to_erase = []

    # Iterate over all block references in the model space
    for block_ref in msp.query('INSERT'):
        explode_block_references(msp, block_ref)
        block_refs_to_erase.append(block_ref)

    # Delete the original block reference
    for block_ref in block_refs_to_erase:
        msp.delete_entity(block_ref)

    doc.saveas(output_file)

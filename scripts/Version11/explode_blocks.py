import ezdxf
from ezdxf.math import Matrix44

def transform_entity(entity, transform):
    """
    Transforms the entity by the given transformation matrix.
    """
    if entity.dxftype() in {'LINE', 'LWPOLYLINE', 'POLYLINE', 'CIRCLE', 'ARC', 'ELLIPSE', 'TEXT', 'MTEXT', 'SPLINE'}:
        entity.transform(transform)
    elif entity.dxftype() == 'INSERT':
        entity.dxf.insert = transform.transform(entity.dxf.insert)
        entity.dxf.rotation += transform.get_rotation()  # Adjust rotation

def inherit_attributes(entity, block_ref):
    """
    Inherit common DXF attributes from the block reference to the entity,
    preserving the entity's original layer if it is not the default layer.
    """
    # Preserve original layer if it's not the default layer (0)
    if entity.dxf.layer == '0' or not entity.dxf.hasattr('layer'):
        entity.dxf.layer = block_ref.dxf.layer

    # Inherit other attributes and prefer 'BYLAYER' over 'BYBLOCK'
    if entity.dxf.color == 0:  # 'BYBLOCK' is represented by 0 in DXF
        entity.dxf.color = block_ref.dxf.color
    if not entity.dxf.hasattr('true_color'):
        entity.dxf.true_color = block_ref.dxf.true_color
    if not entity.dxf.hasattr('linetype'):
        entity.dxf.linetype = block_ref.dxf.linetype
    if not entity.dxf.hasattr('lineweight'):
        entity.dxf.lineweight = block_ref.dxf.lineweight
    if not entity.dxf.hasattr('ltscale'):
        entity.dxf.ltscale = block_ref.dxf.ltscale

def explode_block(insert, msp, doc):
    """
    Explodes a block reference (INSERT) and transfers its entities to the model space non-recursively.
    """
    block_stack = [(insert, Matrix44())]  # Start with the identity matrix

    while block_stack:
        current_insert, block_transform = block_stack.pop()
        block = doc.blocks.get(current_insert.dxf.name)

        for entity in block:
            new_transform = block_transform @ current_insert.matrix44()
            
            if entity.dxftype() == 'INSERT':
                print(f"Exploding nested block: {entity.dxf.name}")
                nested_insert = msp.add_blockref(entity.dxf.name, insert=new_transform.transform(entity.dxf.insert))
                nested_insert.dxf.rotation += current_insert.dxf.rotation  # Properly adjust rotation
                block_stack.append((nested_insert, new_transform))
            else:
                new_entity = entity.copy()
                inherit_attributes(new_entity, current_insert)  # Inherit attributes with layer preservation
                
                # Transform the entity correctly
                new_entity.transform(new_transform)
                msp.add_entity(new_entity)
                print(f"Added entity: {new_entity.dxftype()}")
                
                # Handle attributes if any
                if hasattr(entity, 'attribs'):
                    for attrib in entity.attribs:
                        new_attrib = attrib.copy()
                        inherit_attributes(new_attrib, current_insert)  # Inherit attributes with layer preservation
                        if new_attrib.dxftype() in {'TEXT', 'MTEXT'}:
                            new_attrib.dxf.insert = new_transform.transform(new_attrib.dxf.insert)
                        msp.add_entity(new_attrib)
                        print(f"Added attribute: {new_attrib.dxf.tag}")

def explode_blocks(input_file, output_file):
    try:
        doc = ezdxf.readfile(input_file)
        print("DXF file loaded successfully.")
    except IOError:
        print("Error loading DXF file.")
        return

    msp = doc.modelspace()
    inserts = msp.query('INSERT')
    print(f"Found {len(inserts)} block references to explode.")

    while inserts:
        for insert in inserts:
            block_name = insert.dxf.name
            if block_name in doc.blocks:
                print(f"Exploding block: {block_name}")
                explode_block(insert, msp, doc)
                msp.delete_entity(insert)
                print(f"Removed block reference: {block_name}")
            else:
                print(f"Block {block_name} not found in document blocks.")
        
        inserts = msp.query('INSERT')

    try:
        doc.saveas(output_file)
        print("Modified DXF file saved successfully.")
    except IOError:
        print("Error saving modified DXF file.")
import ezdxf
from ezdxf.math import Matrix44

def transform_entity(entity, transform):
    """
    Transforms the entity by the given transformation matrix.
    """
    if entity.dxftype() in {'LINE', 'LWPOLYLINE', 'POLYLINE', 'CIRCLE', 'ARC', 'ELLIPSE', 'SPLINE', 'TEXT', 'MTEXT'}:
        entity.transform(transform)
    elif entity.dxftype() == 'INSERT':
        entity.dxf.insert = transform.transform(entity.dxf.insert)
        entity.dxf.rotation += transform.get_rotation()  # Adjust rotation

def inherit_attributes(entity, block_ref):
    """
    Inherit common DXF attributes from the block reference, but do not override
    the entity's original layer.
    """
    # Only inherit attributes that should override the original ones
    entity.dxf.color = block_ref.dxf.color
    entity.dxf.true_color = block_ref.dxf.true_color
    entity.dxf.linetype = block_ref.dxf.linetype
    entity.dxf.lineweight = block_ref.dxf.lineweight
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
                nested_insert = msp.add_blockref(entity.dxf.name, insert=entity.dxf.insert)
                nested_insert.dxf.rotation = entity.dxf.rotation  # Set rotation separately
                block_stack.append((nested_insert, new_transform))
            else:
                new_entity = entity.copy()
                inherit_attributes(new_entity, current_insert)  # Inherit attributes without overriding layer
                transform_entity(new_entity, new_transform)
                msp.add_entity(new_entity)
                print(f"Added entity: {new_entity.dxftype()}")
                if hasattr(entity, 'attribs'):
                    for attrib in entity.attribs:
                        new_attrib = attrib.copy()
                        inherit_attributes(new_attrib, current_insert)  # Inherit attributes without overriding layer
                        transform_entity(new_attrib, new_transform)
                        msp.add_entity(new_attrib)
                        print(f"Added attribute: {new_attrib.dxf.tag}")

def main():
    try:
        doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/Testing04_non_recursive/input_05.dxf")
        print("DXF file loaded successfully.")
    except IOError:
        print("Error loading DXF file.")
        return

    msp = doc.modelspace()
    inserts = msp.query('INSERT')
    print(f"Found {len(inserts)} block references to explode.")

    for insert in inserts:
        block_name = insert.dxf.name
        if block_name in doc.blocks:
            print(f"Exploding block: {block_name}")
            explode_block(insert, msp, doc)
            msp.delete_entity(insert)
            print(f"Removed block reference: {block_name}")
        else:
            print(f"Block {block_name} not found in document blocks.")

    try:
        doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/Testing04_non_recursive/output_pos_rot_t03_05.dxf")
        print("Modified DXF file saved as 'output_pos_rot_t03_05.dxf'.")
    except IOError:
        print("Error saving modified DXF file.")

if __name__ == "__main__":
    main()

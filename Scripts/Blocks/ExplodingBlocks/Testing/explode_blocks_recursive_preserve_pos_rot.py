import ezdxf
from ezdxf.math import Matrix44

def transform_entity(entity, transform):
    """
    Transforms the entity by the given transformation matrix.
    """
    if entity.dxftype() in {'LINE', 'LWPOLYLINE', 'POLYLINE', 'CIRCLE', 'ARC', 'ELLIPSE', 'SPLINE', 'TEXT', 'MTEXT'}:
        entity.transform(transform)
    # elif entity.dxftype() == 'TEXT':
    #     entity.dxf.insert = transform.transform(entity.dxf.insert)
    # elif entity.dxftype() == 'MTEXT':
    #     entity.dxf.insert = transform.transform(entity.dxf.insert)
    elif entity.dxftype() == 'INSERT':
        entity.dxf.insert = transform.transform(entity.dxf.insert)
        entity.dxf.rotation += transform.get_rotation()  # Adjust rotation

def explode_block(insert, msp, doc, transform=None):
    """
    Recursively explodes a block reference (INSERT) and transfers its entities to the model space.
    """
    block = doc.blocks.get(insert.dxf.name)
    block_transform = insert.matrix44()
    
    if transform is not None:
        block_transform = transform @ block_transform
    
    for entity in block:
        if entity.dxftype() == 'INSERT':
            nested_block = doc.blocks.get(entity.dxf.name)
            print(f"Exploding nested block: {entity.dxf.name}")
            explode_block(entity, msp, doc, block_transform)
        else:
            new_entity = entity.copy()
            transform_entity(new_entity, block_transform)
            msp.add_entity(new_entity)
            print(f"Added entity: {new_entity.dxftype()}")
            if hasattr(entity, 'attribs'):
                for attrib in entity.attribs:
                    new_attrib = attrib.copy()
                    transform_entity(new_attrib, block_transform)
                    msp.add_entity(new_attrib)
                    print(f"Added attribute: {new_attrib.dxf.tag}")

def main():
    try:
        doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/Testing/input_28.dxf")
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
        doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/Testing/output_pos_rot_28.dxf")
        print("Modified DXF file saved as 'output_09.dxf'.")
    except IOError:
        print("Error saving modified DXF file.")

if __name__ == "__main__":
    main()

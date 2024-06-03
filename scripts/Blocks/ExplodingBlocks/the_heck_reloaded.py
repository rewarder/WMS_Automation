import ezdxf

def explode_block(block, msp, doc):
    """
    Recursively explodes a block reference (INSERT) and transfers its entities to the model space.
    """
    for entity in block:
        # If the entity is another block reference (INSERT), explode it recursively
        if entity.dxftype() == 'INSERT':
            nested_block = doc.blocks.get(entity.dxf.name)
            print(f"Exploding nested block: {entity.dxf.name}")
            explode_block(nested_block, msp, doc)
        else:
            # Clone entity and add to the model space
            new_entity = entity.copy()
            msp.add_entity(new_entity)
            print(f"Added entity: {new_entity.dxftype()}")
            # Handle attributes if the entity has any
            if hasattr(entity, 'attribs'):
                for attrib in entity.attribs:
                    new_attrib = attrib.copy()
                    msp.add_entity(new_attrib)
                    print(f"Added attribute: {new_attrib.dxf.tag}")

def main():
    try:
        # Load the DXF document
        doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/E1866-001Baugrubenplan_Anpassungen_GEOREF.dxf")
        print("DXF file loaded successfully.")
    except IOError:
        print("Error loading DXF file.")
        return

    msp = doc.modelspace()

    # Get all block references (INSERT entities) in the model space
    inserts = msp.query('INSERT')
    print(f"Found {len(inserts)} block references to explode.")

    for insert in inserts:
        block_name = insert.dxf.name
        if block_name in doc.blocks:
            block = doc.blocks.get(block_name)
            print(f"Exploding block: {block_name}")
            # Explode the block reference
            explode_block(block, msp, doc)
            # Remove the original block reference
            msp.delete_entity(insert)
            print(f"Removed block reference: {block_name}")
        else:
            print(f"Block {block_name} not found in document blocks.")

    # Save the modified DXF document
    try:
        doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/exploded_E1866-001Baugrubenplan_Anpassungen_GEOREF.dxf")
        print("Modified DXF file saved as 'exploded_file.dxf'.")
    except IOError:
        print("Error saving modified DXF file.")

if __name__ == "__main__":
    main()

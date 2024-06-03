import ezdxf

def copy_entities_to_new_block(doc, old_block_name, new_block_name):
    old_block = doc.blocks.get(old_block_name)
    if old_block is None:
        raise ValueError(f"Block '{old_block_name}' not found in the DXF document.")
    
    new_block = doc.blocks.new(name=new_block_name)
    
    for entity in old_block:
        new_block.add_entity(entity.copy())

    return new_block

def insert_block_into_modelspace(doc, block_name, position, rotation):
    msp = doc.modelspace()
    block_ref = msp.add_blockref(block_name, position, dxfattribs={'rotation': rotation})
    for attrib in block_ref.attribs:
        block_ref.add_attrib(tag=attrib.dxf.tag, text=attrib.dxf.text, insert=attrib.dxf.insert)
    return block_ref

def delete_block_references(doc, block_name):
    msp = doc.modelspace()
    block_references = msp.query(f'INSERT[name=="{block_name}"]')
    for block_ref in block_references:
        msp.delete_entity(block_ref)

# Main function to execute the tasks
def main():
    # Load your DXF file
    doc = ezdxf.readfile('C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/another.dxf')
    old_block_name = 'OLD_BLOCK_NAME'
    new_block_name = 'NEW_BLOCK_NAME'
    position = (0, 0)
    rotation = 0

    try:
        # Step 1: Copy entities from old block to new block
        new_block = copy_entities_to_new_block(doc, old_block_name, new_block_name)

        # Step 2: Insert the new block into modelspace
        insert_block_into_modelspace(doc, new_block_name, position, rotation)

        # Step 3: Delete all block references of the old block
        delete_block_references(doc, old_block_name)

        # Save the modified DXF file
        doc.saveas('C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/exploded_another.dxf')

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

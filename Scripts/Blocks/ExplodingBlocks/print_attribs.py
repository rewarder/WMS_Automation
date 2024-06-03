import ezdxf

def print_block_attributes(dxf_file_path):
    """
    Prints all attributes from all blocks in the given DXF file.

    :param dxf_file_path: Path to the DXF file.
    """
    # Load the DXF document
    doc = ezdxf.readfile(dxf_file_path)

    # Iterate over all blocks in the BLOCKS section
    for block in doc.blocks:
        print(f"Block name: {block.name}")
        
        # Iterate over all entities in the block
        for entity in block:
            # For ATTDEF (attribute definitions)
            if entity.dxftype() == 'ATTDEF':
                print("  Attribute Definition (ATTDEF) found:")
                print(f"    Tag: {entity.dxf.tag}")
                print(f"    Text: {entity.dxf.text}")
                print(f"    Prompt: {entity.dxf.prompt}")
                print(f"    Insertion Point: {entity.dxf.insert}")
                print(f"    Layer: {entity.dxf.layer}")
            # For ATTRIB (attributes)
            elif entity.dxftype() == 'ATTRIB':
                print("  Attribute (ATTRIB) found:")
                print(f"    Tag: {entity.dxf.tag}")
                print(f"    Text: {entity.dxf.text}")
                print(f"    Insertion Point: {entity.dxf.insert}")
                print(f"    Layer: {entity.dxf.layer}")

# Specify the path to your DXF file
dxf_file_path = 'C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/ExplodingBlocks/100_Erdgeschoss_CraneCam_GEOREF.dxf'

# Call the function to print block attributes
print_block_attributes(dxf_file_path)

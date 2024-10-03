import ezdxf

def list_insert_entities(input_file):
    # Load the DXF document from the input file
    try:
        doc = ezdxf.readfile(input_file)
    except Exception as e:
        print(f'Error reading the DXF file: {e}')
        return

    # Get all layouts in the document
    layouts = doc.layouts

    # Iterate through each layout and list block references
    for layout in layouts:
        print(f'Layout: {layout.name}')
        # Find all INSERT entities (block references)
        insert_entities = layout.query('INSERT')
        if not insert_entities:
            print('  No INSERT entities found.')
        for entity in insert_entities:
            # Print relevant properties of the INSERT entity
            print(f'  INSERT Entity:')
            print(f'    Handle: {entity.dxf.handle}')
            print(f'    Block Name: {entity.dxf.name}')
            print(f'    Position: {entity.dxf.insert}')
            print(f'    Scale: {entity.dxf.scale}')
            print(f'    Rotation: {entity.dxf.rotation}')
            print()

# Example usage in main.py
if __name__ == "__main__":
    input_path = 'intermediate_file4.dxf'
    
    # List all insert entities
    list_insert_entities(input_path)

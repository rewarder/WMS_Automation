import ezdxf

def remove_all_block_references(input_file, output_file):
    # Load the DXF document from the input file
    try:
        doc = ezdxf.readfile(input_file)
    except Exception as e:
        print(f'Error reading the DXF file: {e}')
        return

    # Get all layouts in the document
    layouts = doc.layouts

    # Store removed entities for debugging
    removed_entities = []

    # Iterate through each layout and remove block references
    for layout in layouts:
        # Find all INSERT entities (block references)
        insert_entities = layout.query('INSERT')
        for entity in insert_entities:
            try:
                layout.delete_entity(entity)
                removed_entities.append(entity.dxf.handle)  # Store the handle of the removed entity
                print(f'Removed block reference from layout "{layout.name}": {entity.dxf.handle}')
            except Exception as e:
                print(f'Error removing block reference in layout "{layout.name}": {e}')

    # Print all removed entities after processing
    if removed_entities:
        print(f'\nTotal removed block references: {len(removed_entities)}')
        print('Handles of removed entities:', ', '.join(removed_entities))

    # Save the modified DXF document to the output file
    try:
        doc.saveas(output_file)
        print(f'Modified DXF file saved as: {output_file}')
    except Exception as e:
        print(f'Error saving the document: {e}')

# Example usage in main.py
if __name__ == "__main__":
    input_path = 'intermediate_file4.dxf'
    output_path = 'output_intermediate.dxf'
    
    # Remove all block references
    remove_all_block_references(input_path, output_path)

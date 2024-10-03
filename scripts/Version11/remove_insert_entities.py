import ezdxf

def remove_all_block_references(doc):
    # Get all layouts in the document
    layouts = doc.layouts

    # Iterate through each layout and remove block references
    for layout in layouts:
        # Find all INSERT entities (block references)
        insert_entities = layout.query('INSERT')
        for entity in insert_entities:
            try:
                layout.delete_entity(entity)
                print(f'Removed block reference from layout "{layout.name}".')
            except Exception as e:
                print(f'Error removing block reference in layout "{layout.name}": {e}')

    return doc
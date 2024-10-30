import ezdxf
import traceback

def remove_all_block_references(doc):
    # Get all layouts in the document
    modelspace = doc.modelspace()
    layouts = [modelspace] + list(doc.layouts)

    # Iterate through each layout and remove block references
    for layout in layouts:
        # Find all INSERT entities (block references)
        insert_entities = layout.query('INSERT')
        for entity in insert_entities:
            try:
                # Check if the entity has the 'dxf' attribute
                if hasattr(entity, 'dxf'):
                    layout.delete_entity(entity)
                    print(f'Removed block reference from layout "{layout.name}".')
                else:
                    print(f'Skipping entity without "dxf" attribute in layout "{layout.name}".')
            except Exception as e:
                # Log the error and continue
                print(f'Error removing block reference in layout "{layout.name}": {e}')
                traceback.print_exc()
                continue

    return doc

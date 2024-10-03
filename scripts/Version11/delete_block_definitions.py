import ezdxf

def delete_all_block_definitions(doc):
    # Get all block definitions
    block_records = doc.blocks

    # Collect block names to delete, excluding model and paper space
    blocks_to_delete = [block.name for block in block_records if block.name not in ('*Model_Space', '*Paper_Space')]

    # Remove references to each block in all layouts
    for block_name in blocks_to_delete:
        for layout in doc.layouts:
            try:
                for entity in layout.query(f'INSERT[name=="{block_name}"]'):
                    layout.delete_entity(entity)
            except Exception as e:
                print(f'Error removing references to block "{block_name}" in layout "{layout.name}": {e}')

    # Delete each block definition
    for block_name in blocks_to_delete:
        try:
            # Retrieve the block definition safely
            block = block_records.get(block_name)
            if block is None:
                print(f'Block "{block_name}" not found.')
                continue

            try:
                # Attempt to delete the block
                block_records.delete_block(block_name)
            except ezdxf.DXFBlockInUseError:
                print(f'Block "{block_name}" is still in use.')
            except Exception as e:
                print(f'Error deleting block "{block_name}": {e}')

        except Exception as e:
            print(f'General error while processing block "{block_name}": {e}')

    # Save the modified DXF document
    try:
        return doc
    except Exception as e:
        print(f'Error saving the document: {e}')

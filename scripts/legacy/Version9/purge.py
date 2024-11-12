import ezdxf

def purge_dxf(doc):
    try:
        # Remove all layouts except the model space
        for layout_name in doc.layouts.names():
            if layout_name != 'Model':
                try:
                    doc.layouts.delete(layout_name)
                except Exception as e:
                    print(f"Error deleting layout {layout_name}: {e}")

        # Purge unused layers
        used_layers = {e.dxf.layer for e in doc.modelspace() if hasattr(e.dxf, 'layer')}
        all_layers = {layer.dxf.name for layer in doc.layers}
        unused_layers = all_layers - used_layers

        for layer_name in unused_layers:
            try:
                if layer_name not in ('0', 'Defpoints'):  # '0' and 'Defpoints' are special layers
                    doc.layers.remove(layer_name)
            except Exception as e:
                print(f"Error removing layer {layer_name}: {e}")

        # Purge unused line types
        used_linetypes = set()
        for entity in doc.modelspace():
            if hasattr(entity.dxf, 'linetype'):
                used_linetypes.add(entity.dxf.linetype)

        for entity in doc.blocks:
            for sub_entity in entity:
                if hasattr(sub_entity.dxf, 'linetype'):
                    used_linetypes.add(sub_entity.dxf.linetype)

        # Include other sections if necessary
        # Example: Add entities from paper space, etc.
        
        all_linetypes = {linetype.dxf.name for linetype in doc.linetypes}
        unused_linetypes = all_linetypes - used_linetypes

        for linetype_name in unused_linetypes:
            try:
                if linetype_name not in ('ByLayer', 'ByBlock'):  # 'ByLayer' and 'ByBlock' are default linetypes
                    doc.linetypes.remove(linetype_name)
            except Exception as e:
                print(f"Error removing linetype {linetype_name}: {e}")

        # Purge unused blocks
        used_blocks = {block_name for entity in doc.modelspace() if entity.dxftype() == 'INSERT' for block_name in [entity.dxf.name]}
        
        all_blocks = {block.dxf.name for block in doc.blocks}
        unused_blocks = all_blocks - used_blocks

        for block_name in unused_blocks:
            try:
                if block_name not in ('*Model_Space', '*Paper_Space') and any(entity.dxftype() == 'INSERT' and entity.dxf.name == block_name for entity in doc.modelspace()):  # Check if block is referenced by any entities before deleting
                    doc.blocks.delete_block(block_name)
            except Exception as e:
                print(f"Error deleting block {block_name}: {e}")


    except Exception as e:
        print(f"An error occurred during purging: {e}")

    # return the drawing object for the next function to process it
    return doc

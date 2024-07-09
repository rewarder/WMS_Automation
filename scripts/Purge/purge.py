import ezdxf

def purge_dxf(file_path):
    # Load the DXF file
    doc = ezdxf.readfile(file_path)
    
    # Purge unused layers
    used_layers = {e.dxf.layer for e in doc.modelspace() if hasattr(e.dxf, 'layer')}
    all_layers = {layer.dxf.name for layer in doc.layers}
    unused_layers = all_layers - used_layers

    for layer_name in unused_layers:
        if layer_name not in ('0', 'Defpoints'):  # '0' and 'Defpoints' are special layers
            doc.layers.remove(layer_name)
    
    # Purge unused line types
    used_linetypes = {e.dxf.linetype for e in doc.modelspace() if hasattr(e.dxf, 'linetype')}
    all_linetypes = {linetype.dxf.name for linetype in doc.linetypes}
    unused_linetypes = all_linetypes - used_linetypes

    for linetype_name in unused_linetypes:
        if linetype_name != 'ByLayer':  # 'ByLayer' is a default linetype
            doc.linetypes.remove(linetype_name)
    
    # Purge unused blocks
    used_blocks = {block_name for entity in doc.modelspace() if entity.dxftype() == 'INSERT' for block_name in [entity.dxf.name]}
    all_blocks = {block.dxf.name for block in doc.blocks}
    unused_blocks = all_blocks - used_blocks

    for block_name in unused_blocks:
        if block_name not in ('*Model_Space', '*Paper_Space'):  # Special blocks
            doc.blocks.delete_block(block_name)
    
    # Save the purged DXF file
    output_file_path = file_path.replace('.dxf', '_purged.dxf')
    doc.saveas(output_file_path)
    
    print(f'Purged DXF file saved as: {output_file_path}')

# Example usage
purge_dxf('C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/Purge/input.dxf')

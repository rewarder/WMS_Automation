import ezdxf

def purge_dxf(input_file_path, output_file_path):
    # Load the DXF document
    doc = ezdxf.readfile(input_file_path)

    # Purge unused block definitions
    blocks_to_remove = []
    for block in doc.blocks:
        if len(block) == 0:  # No entities in block
            blocks_to_remove.append(block.name)

    for block_name in blocks_to_remove:
        del doc.blocks[block_name]

    # Purge unused layers
    layers_to_remove = []
    for layer in doc.layers:
        # Check if layer is used in modelspace entities
        if not doc.modelspace().query('LAYER == "{}"'.format(layer.dxf.name)):
            layers_to_remove.append(layer.dxf.name)

    for layer_name in layers_to_remove:
        del doc.layers[layer_name]

    # Purge unused styles
    styles_to_remove = []
    for style in doc.styles:
        # Check if style is used in modelspace entities
        if not doc.modelspace().query('TEXTSTYLE == "{}"'.format(style.dxf.name)):
            styles_to_remove.append(style.dxf.name)

    for style_name in styles_to_remove:
        del doc.styles[style_name]

    # Save the purged DXF file
    doc.saveas(output_file_path)
    print(f"Purged DXF saved as: {output_file_path}")

# Example usage
purge_dxf('intermediate_file4.dxf', 'purged_intermediate_file4.dxf')

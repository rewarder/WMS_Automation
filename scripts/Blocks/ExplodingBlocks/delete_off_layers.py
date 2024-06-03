import ezdxf

def delete_off_layers(input_file_path, output_file_path):
    # Load the DXF file
    doc = ezdxf.readfile(input_file_path)

    # Get the layout (modelspace) of the DXF file
    msp = doc.modelspace()

    # Get all layers that are currently turned off
    off_layers = [layer for layer in doc.layers if not layer.on]

    # Collect the entity handles of entities associated with off layers
    entity_handles_to_delete = set()
    for layer in off_layers:
        for entity in msp.query(f'Layer=="{layer.dxf.name}"'):
            entity_handles_to_delete.add(entity.dxf.handle)
        # Delete the layer
        doc.layers.remove(layer.dxf.name)

    # Delete entities associated with off layers
    for entity in msp:
        if entity.dxf.handle in entity_handles_to_delete:
            msp.delete_entity(entity)

    # Save the modified DXF file
    doc.saveas(output_file_path)

# Example usage
input_file_path = 'input.dxf'
output_file_path = 'output.dxf'
delete_off_layers(input_file_path, output_file_path)

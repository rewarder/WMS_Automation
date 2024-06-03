import ezdxf

def process_dxf_file(input_file_path, output_file_path):
    # Load the DXF file
    doc = ezdxf.readfile(input_file_path)

    # Get the layout (modelspace) of the DXF file
    msp = doc.modelspace()

    # Get all layers that are currently turned on
    on_layers = [layer for layer in doc.layers if layer.on]

    # Collect the entity handles of entities associated with on layers
    entity_handles_to_keep = set()
    for layer in on_layers:
        for entity in msp.query(f'Layer=="{layer.dxf.name}"'):
            entity_handles_to_keep.add(entity.dxf.handle)

    # Delete entities associated with off layers
    for entity in msp:
        if entity.dxf.handle not in entity_handles_to_keep:
            msp.delete_entity(entity)

    # Save the modified DXF file
    doc.saveas(output_file_path)

# Example usage
input_file_path = 'input.dxf'
output_file_path = 'output.dxf'
process_dxf_file(input_file_path, output_file_path)

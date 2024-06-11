import ezdxf

def delete_off_layers_and_entities(input_dxf_file_path, output_dxf_file_path):
    # Load the DXF document
    doc = ezdxf.readfile(input_dxf_file_path)

    # Get the layer table
    layer_table = doc.layers

    # Print details of each layer for debugging before deletion
    print("Before deletion:")
    for layer in layer_table:
        print(f"Layer: {layer.dxf.name}, On: {layer.is_on()}, Off: {layer.is_off()}, Frozen: {layer.is_frozen()}, Locked: {layer.is_locked()}")

    # List to keep track of layers to be deleted
    layers_to_delete = []

    # Identify layers to be deleted
    for layer in layer_table:
        if layer.is_on() == False:  # Explicit check for False
            layers_to_delete.append(layer.dxf.name)
    
    # Collect all entities that are on the layers to be deleted
    entities_to_delete = []
    for entity in doc.modelspace().query('*'):  # Query all entities in the modelspace
        if entity.dxf.layer in layers_to_delete:
            entities_to_delete.append(entity)

    # Delete the identified entities
    for entity in entities_to_delete:
        doc.modelspace().delete_entity(entity)
    
    # Delete the identified layers
    for layer_name in layers_to_delete:
        layer_table.remove(layer_name)
    
    # Save the modified document to a different output file
    doc.saveas(output_dxf_file_path)

    # Print details of each layer for debugging after deletion
    print("After deletion:")
    for layer in layer_table:
        print(f"Layer: {layer.dxf.name}, On: {layer.is_on()}, Off: {layer.is_off()}, Frozen: {layer.is_frozen()}, Locked: {layer.is_locked()}")

# Example usage
input_dxf_file_path = 'C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/Layers/input-test.dxf'
output_dxf_file_path = 'C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/Layers/input-test-mod.dxf'
delete_off_layers_and_entities(input_dxf_file_path, output_dxf_file_path)

import ezdxf

def delete_off_layers_and_entities(doc):
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
        if not layer.is_on():  # Simplified check for False
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
    
    # Print details of each layer for debugging after deletion
    print("After deletion:")
    for layer in layer_table:
        print(f"Layer: {layer.dxf.name}, On: {layer.is_on()}, Off: {layer.is_off()}, Frozen: {layer.is_frozen()}, Locked: {layer.is_locked()}")

    # Return the modified document
    return doc

import ezdxf

def delete_layers_set_to_off(doc):

    # Get the layer table
    layer_table = doc.layers

    # Collect the names of layers set to off
    layers_to_delete = [layer.dxf.name for layer in layer_table if not layer.is_on]

    # Delete the layers set to off and associated entities
    for layer_name in layers_to_delete:
        # Delete the layer
        doc.layers.remove(layer_name)

        # Delete associated entities
        for entity in doc.modelspace().query(f'*[layer=="{layer_name}"]'):
            entity.delete()

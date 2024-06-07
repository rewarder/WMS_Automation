import ezdxf

def delete_layers_set_to_off(dxf_file_path):
    # Load the DXF document
    doc = ezdxf.readfile(dxf_file_path)

    # Get the layer table
    layer_table = doc.layers

    # Collect the names of layers set to off
    layers_to_delete = [layer.dxf.name for layer in layer_table if layer.is_off]

    # Print the names of layers set to off
    if layers_to_delete:
        print("Layers set to off and to be deleted:")
        for layer_name in layers_to_delete:
            print(layer_name)
    else:
        print("No layers set to off found.")

    # Delete the layers set to off
    for layer_name in layers_to_delete:
        # Delete the layer
        doc.layers.remove(layer_name)

    # Save the modified DXF document
    doc.saveas(dxf_file_path)

# Example usage
input_dxf_file_path = 'C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/Layers/modified_splines_test.dxf'
delete_layers_set_to_off(input_dxf_file_path)

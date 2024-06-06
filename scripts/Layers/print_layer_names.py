import ezdxf

def print_layers_set_to_off(dxf_file_path):
    # Load the DXF document
    doc = ezdxf.readfile(dxf_file_path)

    # Get the layer table
    layer_table = doc.layers
    layer_names = [layer.dxf.name for layer in layer_table]
    
    if layer_names:
        print("There actually are some layers")
        for layer_name in layer_names:
            print(layer_name)
    else:
        print("There are no layers")


    # Print the names of layers set to on
    layers_to_print = [layer.dxf.name for layer in layer_table if layer.dxf.is_on]

    if layers_to_print:
        print("Layers set to 'is_on':")
        for layer_name in layers_to_print:
            print(layer_name)
    else:
        print("No layers set to 'is_on' found.")

    # Print the names of layers set to off
    layers_to_print = [layer.dxf.name for layer in layer_table if layer.dxf.is_off]

    if layers_to_print:
        print("Layers set to 'is_off':")
        for layer_name in layers_to_print:
            print(layer_name)
    else:
        print("No layers set to 'is_off' found.")

# Example usage
input_dxf_file_path = 'C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/Layers/input-test.dxf'
print_layers_set_to_off(input_dxf_file_path)

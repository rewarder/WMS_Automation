import ezdxf

def replace_umlauts(text):
    umlaut_mapping = {
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue'
    }
    for umlaut, replacement in umlaut_mapping.items():
        text = text.replace(umlaut, replacement)
    return text

def rename_layers(dxf_file_path):
    # Load the DXF document
    doc = ezdxf.readfile(dxf_file_path)
    
    # Get the layer table
    layer_table = doc.layers
    
    # Create a dictionary to map old layer names to new layer names
    layer_name_mapping = {}
    
    for layer in layer_table:
        old_name = layer.dxf.name
        new_name = old_name.lower().replace(' ', '_')
        new_name = replace_umlauts(new_name)  # Replace German umlauts
        layer_name_mapping[old_name] = new_name
    
    # Now rename the layers
    for old_name, new_name in layer_name_mapping.items():
        if old_name != new_name:
            # Rename the layer
            layer = layer_table.get(old_name)
            layer.dxf.name = new_name
            
            # Update all entities to use the new layer name
            for entity in doc.modelspace().query(f'*[layer=="{old_name}"]'):
                entity.dxf.layer = new_name
    
    # Save the modified DXF document
    doc.saveas(dxf_file_path)

# Example usage
rename_layers('C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/Layers/splines_test.dxf')

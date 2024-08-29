import ezdxf
import re

def replace_umlauts(text):
    umlaut_mapping = {
        'Ä': 'Ae', 
        'Ö': 'Oe', 
        'Ü': 'Ue',
        'ä': 'ae', 
        'ö': 'oe', 
        'ü': 'ue', 
        '.': '_', 
        '-': '_',
        ' ': '_',
        'XR': '',  # General pattern for 'XR' and 'xr'
        'xr': ''
    }
    
    # Replace specific characters
    for umlaut, replacement in umlaut_mapping.items():
        text = re.sub(re.escape(umlaut), replacement, text)
    
    # Remove '$N$' patterns where N is a number
    text = re.sub(r'\$\d+\$', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    return text

def delete_user_coordinate_systems(doc):
    ucs_table = doc.tables.ucs
    for ucs in list(ucs_table):
        ucs_table.remove(ucs)

def rename_layers_in_memory(doc):
    # Delete all user coordinate systems
    delete_user_coordinate_systems(doc)
    
    # Get the layer table
    layer_table = doc.layers
    
    # Create a dictionary to map old layer names to new layer names
    layer_name_mapping = {layer.dxf.name: replace_umlauts(layer.dxf.name) for layer in layer_table}
    
    # Rename layers and update entities
    for old_name, new_name in layer_name_mapping.items():
        if old_name != new_name:
            # Rename the layer to preserve properties
            layer = layer_table.get(old_name)
            layer.dxf.name = new_name
            
            # Update all entities to use the new layer name
            for entity in doc.modelspace().query(f'*[layer=="{old_name}"]'):
                entity.dxf.layer = new_name

    # Delete layers that contain 0 entities
    for layer in list(layer_table):
        layer_name = layer.dxf.name
        if not doc.modelspace().query(f'*[layer=="{layer_name}"]'):
            layer_table.remove(layer_name)
    
    return doc

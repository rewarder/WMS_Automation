import ezdxf
import re

def replace_characters_dictionary(text):
    replacements = {
        'ä': 'ae',
        'Ä': 'ae',
        'ö': 'oe',
        'Ö': 'oe',
        'ü': 'ue',
        'Ü': 'ue',
        '&': '_und_',
        ' ': '_',
        '.': '_'
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text

def rename_layers(doc):
    
    # Get the layer table
    layer_table = doc.layers
    
    # Create a dictionary to map old layer names to new layer names
    layer_name_mapping = {}
    
    for layer in layer_table:
        old_name = layer.dxf.name
        new_name = replace_characters_dictionary(old_name.lower())
        # new_name = re.sub(r'[^a-zA-Z0-9]+', '_', old_name.lower())
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

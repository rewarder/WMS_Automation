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

    # Replace any remaining spaces with underscores
    text = text.replace(' ', '_')

    return text

def rename_layers(doc):
    
    # Get the layer table
    layer_table = doc.layers
    
    # Create a dictionary to map old layer names to new layer names
    layer_name_mapping = {}
    
    for layer in layer_table:
        old_name = layer.dxf.name
        new_name = replace_characters_dictionary(old_name.lower())
        layer_name_mapping[old_name] = new_name
    
    # Now rename the layers
    for old_name, new_name in layer_name_mapping.items():
        if old_name != new_name:
            # Rename the layer
            layer = layer_table.get(old_name)
            new_name_str = str(new_name)  # Ensure new_name is a string
            layer.dxf.name = new_name_str
            
            # Update all entities to use the new layer name
            for entity in doc.modelspace().query(f'*[layer=="{old_name}"]'):
                entity.dxf.layer = new_name_str

            # Delete the old layer
            layer_table.remove(layer)

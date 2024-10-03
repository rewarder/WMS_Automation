import ezdxf
import re

def replace_umlauts(text):
    # Define a regex pattern for umlauts and other characters to replace, including '@'
    pattern = r'Ä|Ö|Ü|ä|ö|ü|\.|-| |XR|xr|@|\$(\d+)\$'
    
    # Define a substitution function
    def substitution(match):
        char = match.group(0)
        if char in ['Ä', 'ä']:
            return 'Ae'
        elif char in ['Ö', 'ö']:
            return 'Oe'
        elif char in ['Ü', 'ü']:
            return 'Ue'
        elif char == '.':
            return '_'
        elif char == '-':
            return '_'
        elif char == ' ':
            return '_'
        elif char in ['XR', 'xr']:
            return ''  # Remove XR/xr
        elif char in ['ß']:
            return 'ss' # Replace 'ß' with 'ss'
        elif char == '@':
            return '_'  # Replace '@' with '_'
        else:
            return ''  # Remove $N$

    # Substitute using the pattern
    text = re.sub(pattern, substitution, text)
    
    # Convert to lowercase
    return text.lower()

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
        try:
            if old_name != new_name:
                # Rename the layer to preserve properties
                layer = layer_table.get(old_name)
                if layer is None:
                    print(f"Layer '{old_name}' not found. Skipping...")
                    continue
                
                layer.dxf.name = new_name
                
                # Update all entities to use the new layer name
                for entity in doc.modelspace().query(f'*[layer=="{old_name}"]'):
                    entity.dxf.layer = new_name
                    
        except Exception as e:
            print(f"Error processing layer '{old_name}': {e}")
            continue  # Proceed to the next layer

    # Delete layers that contain 0 entities
    for layer in list(layer_table):
        layer_name = layer.dxf.name
        if not doc.modelspace().query(f'*[layer=="{layer_name}"]'):
            try:
                layer_table.remove(layer_name)
            except Exception as e:
                print(f"Error removing layer '{layer_name}': {e}")
    
    return doc

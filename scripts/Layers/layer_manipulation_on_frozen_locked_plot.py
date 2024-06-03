import ezdxf

# Open the DXF file
doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Layers/input.dxf")

# Get Model Space (assuming a single Model Space named '0')
model_space = doc.modelspace()

# Extract all entities from Model Space
entities = list(model_space)  # Create a list of all entities

# Extract layer information (assuming unique layer names)
layer_names = set(entity.dxf.layer for entity in entities)  # Set of unique layer names

# Create a new empty DXF document
new_doc = ezdxf.new("AC1032")  # Specify DXF version (optional)
new_modelspace = new_doc.modelspace()

# Define layer colors (optional)
layer_colors = {
    "Achse": 244,  # Red
    "Achsen": 244,  # Red
    "Arbeitsfuge": 250,  # Black
    "Arbeitsfugen": 250,  # Black
    "Betonierfuge": 250,  # Black
    "Betonierfugen": 250,  # Black
    "Bodenplatte": 172,  # Blue (ACI 5)
    "Bruestung": 250,  # Black
    "Decke": 172,  # Blue
    "Sollrissufge": 250,  # Black
    "Sollrissfugen": 250,  # Black
    "Stuetze": 114,  # Green
    "Stuetzen": 250,  # Black
    "Sturz": 250,  # Black
    "Treppe": 250,  # Black
    "Waende Beton": 116,  # Green
    "Waende Beton bewehrt": 116,  # Green
    "Mauerwerk tragend": 114,  # Green
    "Waende oberes Geschoss": 202,  # Blue
    "Waende Mauerwerk": 114,  # Green
    "Waende Mauerwerk tragend": 250,  # Black
}

# Create new layer objects with desired colors in the new document
new_layers = {}
for layer_name in layer_names:
    new_layer = new_doc.layers.new(name=layer_name)
    if layer_name in layer_colors:
        new_layer.dxf.color = layer_colors[layer_name]
 
# Loop through extracted entities and add them to the new Model Space with modified layer assignments
for entity in entities:
    # Get original layer name
    old_layer_name = entity.dxf.layer

    # Choose a new layer (modify logic as needed)
    new_layer_name = old_layer_name  # You can modify layer assignment here based on logic
    
    # Check if the new layer exists
    if new_layer_name not in new_layers:
        new_layers[new_layer_name] = new_doc.layers.get(new_layer_name)
        if new_layers[new_layer_name] is None:  # Create missing layer if needed
            new_layers[new_layer_name] = new_doc.layers.new(name=new_layer_name)

    # Add entity to the new Model Space with the chosen layer
    new_modelspace.add_entity(entity.copy())  # Copy entity to avoid modifying original
    entity.dxf.layer = new_layers[new_layer_name]  # Set layer reference for the copied entity

# Save the modified DXF file
new_doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Layers/modified_file.dxf")

print("DXF file modified and saved!")

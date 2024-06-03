import ezdxf
import os
import shutil  # Import shutil for file operations (renaming, deleting)

# Define layer names and corresponding colors (ACAD Color Index - ACI) using a dictionary {}
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

# Open the DXF file
doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Layers/input.dxf")

# Get layer table
layers = doc.layers

# Loop through layer names in the dictionary
for layer_name in layer_colors:
    # Check if layer exists in the DXF file
    if layer_name in layers:
        # Get the layer object
        layer = layers.get(layer_name)

        # Check if layer object exists (handle potential missing layers)
        if layer is not None:
            # Set the layer's color based on the predefined color
            layer.dxf.color = layer_colors[layer_name]

# Loop through layers in the DXF file
for layer in layers:
    layer.is_frozen = False  # Unfreeze layer
    layer.is_locked = False  # Unlock layer
    layer.is_on = True  # Turn layer on
    # Optional: Save the modified DXF file after each layer to ensure state persistence
    # doc.saveas(output_file)  # Uncomment if needed


    # Set layer properties
    # layer.is_on = True  # Turn layer on
    # layer.is_locked = False  # Unlock layer
    # layer.is_frozen = False  # Unfreeze layer
    # layer.plot = True  # Make layer plottable
    # layer.dxf.linetype = "Continuous"  # Set linetype
    # layer.dxf.lineweight = ezdxf.const.LINEWEIGHT_BYLAYER  # Set lineweight to default
    # layer.transparency = 0  # Set transparency to 0 (opaque)

    # Remove layer description (if any)
    if layer.dxf.hasattr("description"):
        del layer.dxf.description

# Deleting a Layer Definition
doc.layers.remove("Defpoints")

for layer in layers:
    print(f"\nLayer Name: {layer.dxf.name}")
    print(f"  - Description: {layer.dxf.hasattr('description') and layer.dxf.description or '<No description>'}")
    print(f"  - Color: {layer.dxf.color}")  # ACI (AutoCAD Color Index)
    print(f"  - Linetype: {layer.dxf.linetype}")
    print(f"  - Is On: {layer.is_on}")
    print(f"  - Is Frozen: {layer.is_frozen}")
    print(f"  - Is Locked: {layer.is_locked}")
    print(f"  - Plot: {layer.dxf.plot}")
    print(f"  - Lineweight: {layer.dxf.lineweight}")  # Lineweight code
    # Print additional attributes as needed (refer to ezdxf documentation)

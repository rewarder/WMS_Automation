import ezdxf

# Define your DXF file path
dxf_file = "your_file.dxf"

# Define layer names and corresponding colors (ACAD Color Index - ACI)
layer_colors = {
    "Achse": 244,  # Red (ACI 1)
    "Achsen": 250,  # Blue (ACI 5)
    "Arbeitsfuge": 250,  # Green (ACI 3)
    "Arbeitsfugen": 250,  # Blue (ACI 5)
    "Betonierfuge": 250,  # Blue (ACI 5)
    "Betonierfugen": 250,  # Blue (ACI 5)
    "Bodenplatte": 172,  # Blue (ACI 5)
    "Bruestung": 250,  # Blue (ACI 5)
    "Decke": 172,  # Blue (ACI 5)
    "Sollrissufge": 250,  # Blue (ACI 5)
    "Sollrissfugen": 250,  # Blue (ACI 5)
    "Stuetze": 114,  # Blue (ACI 5)
    "Stuetzen": 250,  # Blue (ACI 5)
    "Sturz": 250,  # Blue (ACI 5)
    "Treppe": 250,  # Blue (ACI 5)
    "Waende Beton": 116,  # Blue (ACI 5)
    "Waende Beton bewehrt": 116,  # Blue (ACI 5)
    "Mauerwerk tragend": 114,  # Blue (ACI 5)
    "Waende oberes Geschoss": 202,  # Blue (ACI 5)
    "Waende Mauerwerk": 114,  # Blue (ACI 5)
    "Waende Mauerwerk tragend": 250,  # Blue (ACI 5)
}

# Open the DXF document
doc = ezdxf.readfile(Test.dxf)

# Get the modelspace
msp = doc.modelspace()

# Loop through entities in the modelspace
for entity in msp:
  # Check if the entity has a layer attribute
  if hasattr(entity.dxf, "layer"):
    layer_name = entity.dxf.layer

    # Check if layer name is in our defined list
    if layer_name in layer_colors:
      # Set the entity's color based on the predefined color for the layer
      entity.dxf.color = layer_colors[layer_name]

# Save the modified DXF file with a new name (optional)
doc.saveas("modified_" + dxf_file)

print("DXF file colors updated successfully!")

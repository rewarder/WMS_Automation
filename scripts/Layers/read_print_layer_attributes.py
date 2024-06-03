import ezdxf

# Open the DXF file
doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Layers/input.dxf")

# Get layer table
layers = doc.layers

# Loop through layers and print attributes
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

print("\nAll layer attributes printed!")

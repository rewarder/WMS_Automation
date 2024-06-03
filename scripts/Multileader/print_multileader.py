import ezdxf

def print_leader_entities(dxf_file_path):
    # Load the DXF document
    doc = ezdxf.readfile(dxf_file_path)

    # Access the modelspace
    modelspace = doc.modelspace()

    # Iterate over all entities in the modelspace
    for entity in modelspace:
        # Check if the entity is a 'LEADER'
        if entity.dxftype() == 'LEADER':
            print("LEADER entity found:")
            print(f"  Handle: {entity.dxf.handle}")
            print(f"  Layer: {entity.dxf.layer}")
            print(f"  Color: {entity.dxf.color}")
            # Add any other relevant properties you need to print

# Specify the path to your DXF file
dxf_file_path = 'C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Multileader/51.6.1.2_BF_5_BAUGRUBENAUSHUB__M_1-100_neu_georef.dxf'

# Call the function to print LEADER entities
print_leader_entities(dxf_file_path)

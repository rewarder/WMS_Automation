import ezdxf

def print_hatch_handles(filepath):
    """
    Prints the handles of all hatch entities in a DXF file.

    Args:
        filepath: Path to the DXF file.
    """
    try:
        # Read the DXF file
        doc = ezdxf.readfile(filepath)
        msp = doc.modelspace()

        # Iterate through all entities in the model space
        for entity in msp:
            # Check if the entity is a hatch
            if entity.dxftype() == 'HATCH':
                # Print the handle of the hatch
                print(f"Hatch handle: {entity.dxf.handle}")

    except IOError:
        print(f"Cannot open file: {filepath}")
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file: {filepath}")

# Example usage (replace the placeholder with the path to your DXF file)
filepath = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Bodies/input.dxf"
print_hatch_handles(filepath)

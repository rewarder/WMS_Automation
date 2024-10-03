import ezdxf

def extract_hatches(input_file, output_file):
    """Extracts all hatches from an input .dxf file and saves them to an output .dxf file.

    Args:
        input_file (str): Path to the input .dxf file.
        output_file (str): Path to the output .dxf file.

    Returns:
        None
    """

    try:
        doc = ezdxf.readfile(input_file)
    except IOError:
        print(f"Error reading file: {input_file}")
        return

    msp = doc.modelspace()  # Use modelspace for simplicity
    hatches = [hatch for hatch in msp if hatch.dxftype() == 'HATCH']

    if hatches:
        # Create a new DXF document for the output hatches
        out_doc = ezdxf.new(dxfversion=doc.dxfversion)
        out_msp = out_doc.modelspace()

        # Copy the hatches to the output document
        for hatch in hatches:
            out_msp.add_entity(hatch.copy())

        # Save the output document
        out_doc.saveas(output_file)

        print(f"Saved {len(hatches)} hatches to {output_file}")
    else:
        print(f"No hatches found in {input_file}")

if __name__ == "__main__":
    input_file = "hatches_renamed.dxf"  # Replace with your input file path
    output_file = "hatches_renamed_output.dxf"  # Replace with your desired output file path

    extract_hatches(input_file, output_file)
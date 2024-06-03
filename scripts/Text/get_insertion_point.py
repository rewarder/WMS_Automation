import ezdxf

def retrieve_insertion_point(input_file):
    """Retrieves the insertion point of text entities from a DXF file."""
    doc = ezdxf.readfile(input_file)

    # Extract text entities from the model space
    msp = doc.modelspace()
    text_entities = [text for text in msp.query('TEXT')]

    # Iterate through each text entity
    for text in text_entities:
        # Retrieve insertion point
        insertion_point = text.dxf.insert
        x = insertion_point[0]
        y = insertion_point[1]

        # Print insertion point coordinates
        print(f"Insertion point: ({x}, {y})")

# Specify the input DXF file path
input_file_path = "Text/Text.dxf"

# Retrieve insertion points for text entities
retrieve_insertion_point(input_file_path)

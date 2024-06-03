import ezdxf

def extract_text_with_insertion_points(input_file):
    # Create an empty list to store text and its insertion points
    text_data = []

    # Read the DXF file
    doc = ezdxf.readfile(input_file)

    # Get the model space
    msp = doc.modelspace()

    # Iterate through text entities in the model space
    for text_entity in msp.query('TEXT'):
        text = text_entity.dxf.text
        insertion_point = text_entity.dxf.insert

        # Append text and its insertion point to the list
        text_data.append((text, insertion_point))

    return text_data

if __name__ == "__main__":
    # Specify the input DXF file path
    input_dxf_file = "Text/Text.dxf"

    # Extract text with insertion points from the input DXF file
    extracted_text = extract_text_with_insertion_points(input_dxf_file)

    # Print the extracted text and insertion points
    for text, insertion_point in extracted_text:
        print(f"Text: {text}, Insertion Point: {insertion_point}")
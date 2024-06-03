import ezdxf

def convert_text_to_lines(doc):
    msp = doc.modelspace()

    entities = list(msp)

    for entity in entities:
        if entity.dxftype() == "TEXT":
            insertion_point = entity.dxf.insert
            text_height = entity.dxf.height
            text_value = entity.dxf.text

            # Calculate the width of the text bounding box
            if entity.dxf.hasattr('width'):
                text_width = entity.dxf.width
            else:
                text_width = len(text_value) * entity.dxf.height * 0.7  # Approximate width

            # Create lines that represent the outline of the text bounding box
            lines = [
                ((insertion_point[0], insertion_point[1]), (insertion_point[0] + text_width, insertion_point[1])),
                ((insertion_point[0], insertion_point[1]), (insertion_point[0], insertion_point[1] + text_height)),
                ((insertion_point[0], insertion_point[1]), (insertion_point[0] + text_width, insertion_point[1] + text_height)),
                ((insertion_point[0] + text_width, insertion_point[1]), (insertion_point[0] + text_width, insertion_point[1] + text_height)),
            ]

            # Add the lines to the modelspace
            for line in lines:
                start_point, end_point = line
                start_x, start_y = start_point
                end_x, end_y = end_point
                msp.add_line((start_x, start_y), (end_x, end_y))

            # Remove the original text entity
            # entity.unlink()

    # Save the modified DXF file
    doc.saveas(output_dxf_file)

if __name__ == "__main__":
    # Specify the input DXF file and output DXF file
    input_dxf_file = "some_random_text.dxf"
    output_dxf_file = "output_file.dxf"

    # Load the DXF file
    doc = ezdxf.readfile(input_dxf_file)

    # Convert text to lines
    convert_text_to_lines(doc)

    print(f"Conversion completed. Output saved to {output_dxf_file}")

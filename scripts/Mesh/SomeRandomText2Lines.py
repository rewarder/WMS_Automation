import pathlib
import ezdxf
from ezdxf.addons import text2path
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.fonts import fonts
from ezdxf.math import Matrix44
from ezdxf import zoom, path

CWD = pathlib.Path("~/Desktop/Outbox").expanduser()
if not CWD.exists():
    CWD = pathlib.Path(".")

FONT = fonts.FontFace(family="Arial")

def extract_text_from_dxf(input_file):
    text_content = ""

    # Read the DXF file
    doc = ezdxf.readfile(input_file)

    # Get the text entities from the model space
    msp = doc.modelspace()
    text_entities = msp.query('TEXT')

    # Iterate through text entities and extract text content
    for text_entity in text_entities:
        text_content += text_entity.dxf.text + "\n"

    return text_content

def text_to_boundry_lines(text_content):
    doc = ezdxf.new()
    msp = doc.modelspace()

    paths = text2path.make_paths_from_str(
        text_content, font=FONT, size=4, m=Matrix44.translate(2, 1.5, 0)
    )
    for path in paths:
        # Create a polyline from the path
        polyline = msp.add_lwpolyline(points=path.flattening(0.1))
        
        # Set color to make it visible (optional)
        # polyline.dxf.color = GfxAttribs(color=ezdxf.colors.RED)

    return doc


def polylines_to_lines(polyline, output_file):
    msp = doc.modelspace()
    output_doc = ezdxf.new()
    output_msp = output_doc.modelspace()

    # Iterate through all polylines in the input file
    for polyline in msp.query('LWPOLYLINE'):
        # Extract vertices from the polyline
        vertices = list(polyline.vertices())

        # Create lines between consecutive vertices
        for i in range(len(vertices) - 1):
            start_point = vertices[i]
            end_point = vertices[i + 1]

            # Create a line
            line = output_msp.add_line(start_point, end_point)

            # Copy attributes from the original polyline (optional)
            line.dxf.color = polyline.dxf.color
            # Copy other attributes as needed...

    # Save the output DXF file
    output_doc.saveas(output_file)


if __name__ == "__main__":
    # Specify the input DXF file path
    input_dxf_file = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Text/some_random_text.dxf"
    output_file_path = CWD / "SomeRandomText2Lines.dxf"

    # Extract text from the input DXF file
    extracted_text = extract_text_from_dxf(input_dxf_file)

    # Call text_to_boundry_lines() with extracted text
    doc = text_to_boundry_lines(extracted_text)

    # Convert polyline to lines and save the result
    polylines_to_lines(doc, output_file_path)

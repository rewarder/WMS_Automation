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

def extract_text_and_positions(input_file):
  text_content = []
  positions = []

  # Read the DXF file
  doc = ezdxf.readfile(input_file)

  # Get the text entities from the model space
  msp = doc.modelspace()
  text_entities = msp.query('TEXT')

  # Iterate through text entities, extract text and insertion point
  for text_entity in text_entities:
    text_content.append(text_entity.dxf.text)
    positions.append(text_entity.dxf.insert)

  return text_content, positions


def text_to_boundry_lines(text_content, positions):
  doc = ezdxf.new()
  msp = doc.modelspace()
  FONT = fonts.FontFace(family="Arial")

  for i, text in enumerate(text_content):
    # Use the position from positions list
    position = positions[i]
    paths = text2path.make_paths_from_str(
        text, font=FONT, size=4, m=Matrix44.translate(position[0], position[1], 0)
    )
    for path in paths:
      # Create a polyline from the path
      polyline = msp.add_lwpolyline(points=path.flattening(0.1))

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
    input_dxf_file = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Text/Text.dxf"
    output_file_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Text/SomeRandomText2Lines.dxf"

    # Extract text and positions
    extracted_text, positions = extract_text_and_positions(input_dxf_file)

    # Call text_to_boundry_lines with extracted text and positions
    doc = text_to_boundry_lines(extracted_text, positions)

    # Convert polyline to lines and save the result
    polylines_to_lines(doc, output_file_path)

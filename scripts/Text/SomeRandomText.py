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

    zoom.extents(msp)
    doc.saveas(CWD / "some_random_text_converted.dxf")

if __name__ == "__main__":
    # Specify the input DXF file path
    input_dxf_file = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Text/some_random_text.dxf"

    # Extract text from the input DXF file
    extracted_text = extract_text_from_dxf(input_dxf_file)

    # Call text_to_boundry_lines() with extracted text
    text_to_boundry_lines(extracted_text)

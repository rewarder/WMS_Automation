import pathlib
from pathlib import Path
import ezdxf
from ezdxf.addons import text2path
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.fonts import fonts
from ezdxf.math import Matrix44
from ezdxf import zoom, path
from ezdxf.render import hatching

CWD = pathlib.Path("~/Desktop/Outbox").expanduser()
if not CWD.exists():
    CWD = pathlib.Path(".")



def text_to_boundry_lines():
    doc = ezdxf.new()
    msp = doc.modelspace()

    paths = text2path.make_paths_from_str(
        SAMPLE_STRING, font=FONT, size=4, m=Matrix44.translate(2, 1.5, 0)
    )
    for path in paths:
        # Create a polyline from the path
        polyline = msp.add_lwpolyline(points=path.flattening(0.1))
        
        # Set color to make it visible (optional)
        # polyline.dxf.color = GfxAttribs(color=ezdxf.colors.RED)

    zoom.extents(msp)
    doc.saveas(CWD / "text2boundarylines.dxf")






# Script 2: Polylines to Lines
CWD = Path(__file__).parent

def polylines_to_lines(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    msp = doc.modelspace()

    # Create a new DXF file object for the output
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

# Specify the input and output file paths
input_file_path = CWD / "some_random_text.dxf"
output_file_path = CWD / "Text2Lines.dxf"

# Convert polylines to lines and save the result
polylines_to_lines(input_file_path, output_file_path)
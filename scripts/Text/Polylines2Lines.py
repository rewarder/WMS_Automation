import ezdxf
from pathlib import Path

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
input_file_path = CWD / "text2boundarylines2lines.dxf"
output_file_path = CWD / "Polylines2lines.dxf"

# Convert polylines to lines and save the result
polylines_to_lines(input_file_path, output_file_path)
import ezdxf
from ezdxf.math import Vec3
from ezdxf import colors
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.render import forms

def parse_polylines_and_create_mesh(input_file, output_file):
    """Parses a DXF file containing polylines and creates a mesh based on their vertices."""
    doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Mesh/input-file.dxf")

    # Extract polylines from the model space
    msp = doc.modelspace()
    polylines = [polyline for polyline in msp.query('LWPOLYLINE')]

    # Create an empty list to store mesh vertices
    mesh_vertices = []

    # Iterate through each polyline
    for polyline in polylines:
        # Extract vertices from the polyline
        vertices = list(polyline.vertices())

        # Create 3D vertices by converting 2D coordinates
        for vertex in vertices:
            x, y = vertex
            mesh_vertices.append(Vec3(x, y, 0))

    # Create a mesh object from the vertices
    mesh = ezdxf.mesh.Mesh(mesh_vertices)

    return mesh

def save_mesh_to_dxf(mesh, output_file):
    """Saves a mesh to a DXF file."""
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Add the mesh to the DXF file
    msp.add_mesh(mesh)

    # Save the DXF file
    doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Mesh/output-file.dxf")

# Specify the input DXF file path
input_file_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Mesh/input-data.dxf"
output_file_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Mesh/output-file.dxf"

# Parse the DXF file and create the mesh
mesh = parse_polylines_and_create_mesh(input_file_path, output_file_path)

# Save the mesh to the output DXF file
save_mesh_to_dxf(mesh, output_file_path)

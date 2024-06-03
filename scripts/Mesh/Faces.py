import ezdxf
from ezdxf.math import Vec3

def parse_polylines_and_create_faces(input_file):
    doc = ezdxf.readfile(input_file)

    # Extract polylines from the model space
    msp = doc.modelspace()
    polylines = [polyline for polyline in msp.query('LWPOLYLINE')]

    # Create an empty list to store 3D faces vertices
    faces_vertices = []

    # Iterate through each polyline
    for polyline in polylines:
        # Extract vertices from the polyline
        vertices = list(polyline.vertices())

        # Create 3D vertices by converting 2D coordinates
        face_vertices = [Vec3(x, y, 0) for x, y in vertices]

        # Append the vertices to the list
        faces_vertices.extend(face_vertices)

    return faces_vertices

def create_faces(mesh_vertices):
    # Create 3D faces using the vertices
    faces = []
    for i in range(0, len(mesh_vertices), 4):
        # Create a 3D face for every set of 4 vertices
        face = mesh_vertices[i:i+4]
        if len(face) == 4:
            faces.append(face)

    return faces

def save_faces_to_dxf(faces, output_file):
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Add 3D faces to the DXF file
    for face_vertices in faces:
        if len(face_vertices) == 3:
            msp.add_3dface(face_vertices)
        elif len(face_vertices) == 4:
            msp.add_3dface(face_vertices[:3])  # Remove the dxfattribs parameter

    # Save the DXF file
    doc.saveas(output_file)

# Specify the input DXF file path
input_file_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Mesh/input-file.dxf"
output_file_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Mesh/output-file.dxf"

# Parse the DXF file and create 3D faces
mesh_vertices = parse_polylines_and_create_faces(input_file_path)
faces = create_faces(mesh_vertices)

# Save the 3D faces to the output DXF file
save_faces_to_dxf(faces, output_file_path)

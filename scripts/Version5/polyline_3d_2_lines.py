import ezdxf

def is_2d_polyline(polyline):
    # Check if the polyline is closed
    if not polyline.is_closed:
        return False

    # Check if all vertices have the same z-coordinate (2D polyline)
    z_coords = set(point[2] for point in polyline.points())
    if len(z_coords) == 1:
        return True
    else:
        return False

def convert_3d_polylines_to_lines(doc):
    msp = doc.modelspace()

    # Iterate through all entities in the modelspace
    for entity in msp:
        if entity.dxftype() == 'POLYLINE' and not is_2d_polyline(entity):
            # Get the vertices of the 3D polyline
            vertices = list(entity.points())

            # Get attributes from the original polyline
            layer = entity.dxf.layer
            color = entity.dxf.color

            # Convert the 3D polyline to lines by connecting consecutive vertices
            for i in range(len(vertices) - 1):
                start_point = vertices[i]
                end_point = vertices[i + 1]

                # Add a line with the same attributes as the original polyline
                msp.add_line(start_point, end_point, dxfattribs={'layer': layer, 'color': color})

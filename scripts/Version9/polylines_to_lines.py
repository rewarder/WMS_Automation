import ezdxf

def polylines_to_lines(doc):
    msp = doc.modelspace()

    for polyline in msp.query("LWPOLYLINE"):
        vertices = list(polyline.vertices())
        # Store the color to apply it to the lines
        color = polyline.dxf.color
        # Remove the polyline after extracting its vertices
        msp.delete_entity(polyline)

        for i in range(len(vertices) - 1):
            start_point = vertices[i]
            end_point = vertices[i + 1]

            line = msp.add_line(start_point, end_point)
            line.dxf.color = color
    
    return(doc)
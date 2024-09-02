import ezdxf

def trace_solid_entities(doc):
    """
    Trace BODY entities in the given DXF document and return a new DXF document with lines connecting the vertices.

    :param doc: A loaded DXF document (ezdxf.document.DXFDocument).
    :return: A new DXF document with traced lines.
    """
    msp = doc.modelspace()

    # Create a new DXF document for output
    output_doc = ezdxf.new()
    output_msp = output_doc.modelspace()

    # Iterate over BODY entities in the model space
    for body in msp.query('SOLID'):
        # Get the vertices of the body
        vertices = body.vertices()
        
        # Check if vertices are available
        if vertices:
            # Print the vertices' locations
            print(f"Body vertices:")
            for vertex in vertices:
                print(vertex)  # Print the location of each vertex
            
            # Create lines connecting each vertex
            for i in range(len(vertices)):
                start_point = vertices[i]
                end_point = vertices[(i + 1) % len(vertices)]  # Wrap around to the first vertex
                output_msp.add_line(start_point, end_point)

    return output_doc

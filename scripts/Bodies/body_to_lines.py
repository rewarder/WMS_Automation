import ezdxf

def trace_solid_entities(input_dxf, output_dxf):
    # Load the DXF document
    doc = ezdxf.readfile(input_dxf)
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
    
    # Save the new DXF file
    output_doc.saveas(output_dxf)
    print(f"Tracing completed. Output saved as '{output_dxf}'.")

# Example usage
if __name__ == "__main__":
    input_dxf_file = 'bodies.dxf'  # Replace with your input DXF file
    output_dxf_file = 'output.dxf'  # Desired output DXF file
    trace_body_entities(input_dxf_file, output_dxf_file)

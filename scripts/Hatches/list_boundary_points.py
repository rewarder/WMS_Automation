import ezdxf
import math

def list_hatch_boundary_points(dxf_file):
    # Load the DXF file
    doc = ezdxf.readfile(dxf_file)
    
    # Create a dictionary to store boundary points for each hatch
    hatch_boundaries = {}

    # Iterate through all entities in the model space
    for entity in doc.modelspace().query('HATCH'):
        hatch_id = str(entity.dxf.handle)  # Unique identifier for the hatch
        points = []

        # Get the boundary paths of the hatch
        for boundary in entity.paths:
            if isinstance(boundary, ezdxf.entities.PolylinePath):
                # For polyline boundaries, extract points
                points.extend(boundary.vertices)
            elif isinstance(boundary, ezdxf.entities.CirclePath):
                # Handle circular boundaries
                center = boundary.center
                radius = boundary.radius
                # Approximate circle with a set of points
                circle_points = [
                    (center[0] + radius * math.cos(theta), center[1] + radius * math.sin(theta))
                    for theta in [i * (2 * math.pi / 100) for i in range(100)]
                ]
                points.extend(circle_points)

        # Store the points for this hatch
        hatch_boundaries[hatch_id] = points

    return hatch_boundaries

def save_hatch_boundaries_to_dxf(hatch_boundaries, output_file):
    # Create a new DXF document
    new_doc = ezdxf.new()

    # Add a new modelspace
    msp = new_doc.modelspace()

    for hatch_id, points in hatch_boundaries.items():
        # Create lines connecting the points
        for i in range(len(points)):
            start_point = points[i]
            end_point = points[(i + 1) % len(points)]  # Connect last point to the first
            msp.add_line(start_point, end_point)

    # Save the new DXF document
    new_doc.saveas(output_file)

# Example usage
if __name__ == "__main__":
    hatch_boundaries = list_hatch_boundary_points('hatches_renamed_output.dxf')
    save_hatch_boundaries_to_dxf(hatch_boundaries, 'hatches.dxf')

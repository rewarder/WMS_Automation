import ezdxf
import math

def list_hatch_boundary_points(doc):
    # Create a dictionary to store boundary points and attributes for each hatch
    hatch_boundaries = {}

    # Iterate through all entities in the model space
    for entity in doc.modelspace().query('HATCH'):
        hatch_id = str(entity.dxf.handle)  # Unique identifier for the hatch
        points = []
        attributes = {
            'color': entity.dxf.color,
            'layer': entity.dxf.layer,
            'linetype': entity.dxf.linetype,
        }

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

        # Store the points and attributes for this hatch
        hatch_boundaries[hatch_id] = (points, attributes)

    return hatch_boundaries, doc

def save_hatch_boundaries_to_dxf(hatch_boundaries, doc):
    # Add a new modelspace if needed
    msp = doc.modelspace()

    for hatch_id, (points, attributes) in hatch_boundaries.items():
        # Create lines connecting the points
        for i in range(len(points)):
            start_point = points[i]
            end_point = points[(i + 1) % len(points)]  # Connect last point to the first
            
            # Create a line with the attributes from the hatch
            line = msp.add_line(start_point, end_point)
            line.dxf.color = attributes['color']
            line.dxf.layer = attributes['layer']
            line.dxf.linetype = attributes['linetype']

    return doc

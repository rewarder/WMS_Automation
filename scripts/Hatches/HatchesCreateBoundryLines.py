import ezdxf
import math

def create_hatch_boundary_for_all_hatches(filepath):
    try:
        doc = ezdxf.readfile(filepath)
        msp = doc.modelspace()

        for hatch in msp.query('HATCH'):
            boundary_points = []

            for path in hatch.paths:
                for edge in path.edges:
                    if edge.EDGE_TYPE == 'LineEdge':
                        boundary_points.append(edge.start)
                        # For the last edge, also include the endpoint
                        if edge is path.edges[-1]:
                            boundary_points.append(edge.end)
                    elif edge.EDGE_TYPE == 'ArcEdge':
                        # Approximate arc with polyline vertices
                        center = edge.center
                        radius = edge.radius
                        start_angle = edge.start_angle
                        end_angle = edge.end_angle
                        is_counter_clockwise = edge.ccw
                        num_segments = max(2, int(radius * abs(end_angle - start_angle) / 10))  # Adjust num_segments as needed
                        angle_step = (end_angle - start_angle) / num_segments
                        if not is_counter_clockwise:
                            angle_step = -angle_step
                        for i in range(num_segments + 1):
                            angle = start_angle + i * angle_step
                            angle_rad = math.radians(angle)
                            point = ezdxf.math.Vec2(radius * math.cos(angle_rad) + center.x,
                                                    radius * math.sin(angle_rad) + center.y)
                            boundary_points.append(point)

            if boundary_points:
                # Ensure the polyline is closed by repeating the first point at the end
                if boundary_points[0] != boundary_points[-1]:
                    boundary_points.append(boundary_points[0])
                boundary = msp.add_lwpolyline(boundary_points)
                boundary.dxf.layer = "Hatch_Boundaries"
                boundary.dxf.color = 7

        doc.saveas(filepath)
        print(f"Boundary lines created for all hatches in {filepath}.")

    except Exception as e:
        print(f"Error processing file: {filepath}")
        print(f"Error message: {e}")

# Example usage
filepath = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Test/Schraff.dxf"
create_hatch_boundary_for_all_hatches(filepath)

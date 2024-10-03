import ezdxf
import math

def create_hatch_boundary(input_path, output_path):
    try:
        doc = ezdxf.readfile(input_path)
        msp = doc.modelspace()

        for hatch in msp.query('HATCH'):
            for path in hatch.paths:
                boundary_points = []

                # Check if the path is a polyline path
                if path.path_type_flags & 1:  # Polyline path type
                    for vertex in path.vertices:
                        boundary_points.append((vertex[0], vertex[1]))

                # Check if the path is an edge path
                if path.path_type_flags & 2:  # Edge path type
                    for edge in path.edges:
                        if edge.EDGE_TYPE == 'LineEdge':
                            boundary_points.append(edge.start)
                            boundary_points.append(edge.end)
                        elif edge.EDGE_TYPE == 'ArcEdge':
                            center = edge.center
                            radius = edge.radius
                            start_angle = math.radians(edge.start_angle)
                            end_angle = math.radians(edge.end_angle)
                            num_segments = 20
                            angle_step = (end_angle - start_angle) / num_segments
                            for i in range(num_segments + 1):
                                angle = start_angle + i * angle_step
                                x = center[0] + radius * math.cos(angle)
                                y = center[1] + radius * math.sin(angle)
                                boundary_points.append((x, y))
                        elif edge.EDGE_TYPE == 'EllipseEdge':
                            center = edge.center
                            major_axis = edge.major_axis
                            ratio = edge.ratio
                            start_angle = edge.start_angle
                            end_angle = edge.end_angle
                            is_counter_clockwise = edge.ccw
                            num_segments = max(8, int(major_axis.magnitude * abs(end_angle - start_angle) / 10))
                            angle_step = (end_angle - start_angle) / num_segments
                            if not is_counter_clockwise:
                                angle_step = -angle_step
                            for i in range(num_segments + 1):
                                angle = start_angle + i * angle_step
                                angle_rad = math.radians(angle)
                                point = ezdxf.math.ellipse_parametrization(center, major_axis, ratio, angle_rad)
                                boundary_points.append(point)
                        elif edge.EDGE_TYPE == 'SplineEdge':
                            num_segments = 20
                            spline_points = edge.spline.approximate(num_segments)
                            boundary_points.extend(spline_points)

                if boundary_points:
                    # Create a polyline for each boundary path
                    boundary = msp.add_lwpolyline(boundary_points, is_closed=True)
                    boundary.dxf.layer = "Hatch_Boundaries"
                    boundary.dxf.color = 7

            # Manually create edge paths if needed
            new_path = hatch.paths.add_edge_path()
            for i in range(len(boundary_points) - 1):
                start = boundary_points[i]
                end = boundary_points[i + 1]
                new_path.add_line(start, end)

        doc.saveas(output_path)

    except Exception as e:
        print(f"Error processing file: {input_path}")
        print(f"Error message: {e}")

# Example of how to call the function
create_hatch_boundary('hatches_renamed_output.dxf', 'hatches.dxf')

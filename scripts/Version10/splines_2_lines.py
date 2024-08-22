import ezdxf
from ezdxf.math import ConstructionPolyline

def splines_2_lines(doc, flattening_distance=0.01):
    msp = doc.modelspace()

    # Query all SPLINE entities in the model space
    splines = msp.query("SPLINE")

    # Convert each SPLINE to a POLYLINE
    for spline in splines:
        # Flatten the spline to a series of points
        polyline_points = spline.flattening(flattening_distance)
        
        # Create a new LWPOLYLINE entity in the model space
        polyline = msp.add_lwpolyline(polyline_points, close=False)
        
        # Copy attributes from the spline to the polyline
        polyline.dxf.layer = spline.dxf.layer
        polyline.dxf.color = spline.dxf.color
        polyline.dxf.linetype = spline.dxf.linetype
        polyline.dxf.lineweight = spline.dxf.lineweight
        polyline.dxf.ltscale = spline.dxf.ltscale

        # Delete the original spline
        msp.delete_entity(spline)

        # Convert the polyline to individual lines
        vertices = list(polyline.vertices())
        for i in range(len(vertices) - 1):
            start_point = vertices[i]
            end_point = vertices[i + 1]

            line = msp.add_line(start_point, end_point)
            
            # Copy attributes from the polyline to the line
            line.dxf.layer = polyline.dxf.layer
            line.dxf.color = polyline.dxf.color
            line.dxf.linetype = polyline.dxf.linetype
            line.dxf.lineweight = polyline.dxf.lineweight
            line.dxf.ltscale = polyline.dxf.ltscale

        # Delete the polyline after converting to lines
        msp.delete_entity(polyline)

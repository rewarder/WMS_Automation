import ezdxf
import math

def approximate_ellipse_with_lines(msp, center, major_axis, ratio, start_param, end_param, dxfattribs, segments=100):
    for i in range(segments):
        t1 = start_param + (end_param - start_param) * i / segments
        t2 = start_param + (end_param - start_param) * (i + 1) / segments
        p1 = calculate_ellipse_point(center, major_axis, ratio, t1)
        p2 = calculate_ellipse_point(center, major_axis, ratio, t2)
        msp.add_line(p1, p2, dxfattribs=dxfattribs)

def calculate_ellipse_point(center, major_axis, ratio, t):
    a = major_axis.magnitude
    b = a * ratio
    angle = math.atan2(major_axis.y, major_axis.x)

    x = a * math.cos(t)
    y = b * math.sin(t)

    x_rot = x * math.cos(angle) - y * math.sin(angle)
    y_rot = x * math.sin(angle) + y * math.cos(angle)

    return center.x + x_rot, center.y + y_rot

def redraw_ellipses(doc):
    msp = doc.modelspace()
    ellipses_to_remove = []

    for entity in msp.query('ELLIPSE'):
        center = entity.dxf.center
        major_axis = entity.dxf.major_axis
        ratio = entity.dxf.ratio
        start_param = entity.dxf.start_param
        end_param = entity.dxf.end_param

        # Get DXF attributes to apply to the lines
        dxfattribs = {
            'layer': entity.dxf.layer,
            'color': entity.dxf.color,
            # Add other attributes if needed
        }

        approximate_ellipse_with_lines(msp, center, major_axis, ratio, start_param, end_param, dxfattribs)
        ellipses_to_remove.append(entity)

    for ellipse in ellipses_to_remove:
        msp.delete_entity(ellipse)

    return doc
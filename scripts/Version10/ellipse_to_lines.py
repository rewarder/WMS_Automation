import ezdxf
import math

def copy_entity(entity, msp):
    entity_type = entity.dxftype()
    if entity_type == 'ELLIPSE':
        msp.add_ellipse(
            center=entity.dxf.center,
            major_axis=entity.dxf.major_axis,
            ratio=entity.dxf.ratio,
            start_param=entity.dxf.start_param,
            end_param=entity.dxf.end_param,
            dxfattribs=entity.dxfattribs()
        )
    else:
        msp.add_entity(entity.copy())

def approximate_ellipse_with_lines(msp, center, major_axis, ratio, start_param, end_param, segments=100):
    # Calculate the points along the ellipse
    for i in range(segments):
        t1 = start_param + (end_param - start_param) * i / segments
        t2 = start_param + (end_param - start_param) * (i + 1) / segments
        p1 = calculate_ellipse_point(center, major_axis, ratio, t1)
        p2 = calculate_ellipse_point(center, major_axis, ratio, t2)
        msp.add_line(p1, p2)

def calculate_ellipse_point(center, major_axis, ratio, t):
    # Calculate the coordinates of a point on the ellipse at parameter t
    a = major_axis.magnitude
    b = a * ratio

    # Get the rotation angle of the ellipse's major axis
    angle = math.atan2(major_axis.y, major_axis.x)

    x = a * math.cos(t)
    y = b * math.sin(t)

    # Rotate the point by the angle of the major axis
    x_rot = x * math.cos(angle) - y * math.sin(angle)
    y_rot = x * math.sin(angle) + y * math.cos(angle)

    # Translate the point to the ellipse's center
    return center.x + x_rot, center.y + y_rot

def redraw_ellipses(doc):
    msp = doc.modelspace()

    # Create a new DXF document for output
    new_doc = ezdxf.new()
    new_msp = new_doc.modelspace()

    # Copy all entities from input to the new document
    for entity in msp:
        copy_entity(entity, new_msp)

    # Extract and approximate ellipses with lines
    for entity in msp.query('ELLIPSE'):
        # Get ellipse parameters
        center = entity.dxf.center
        major_axis = entity.dxf.major_axis
        ratio = entity.dxf.ratio
        start_param = entity.dxf.start_param
        end_param = entity.dxf.end_param

        # Approximate the ellipse with lines
        approximate_ellipse_with_lines(new_msp, center, major_axis, ratio, start_param, end_param)

    return new_doc

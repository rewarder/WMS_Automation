import ezdxf
from ezdxf.math import Vec3

# Define the boundary box for Switzerland in LV95 coordinates
switzerland_boundary = {
    'min_x': 2480000,
    'max_x': 2830000,
    'min_y': 1070000,
    'max_y': 1290000
}

def is_inside_switzerland_boundary(point):
    x, y, _ = point
    return switzerland_boundary['min_x'] <= x <= switzerland_boundary['max_x'] and switzerland_boundary['min_y'] <= y <= switzerland_boundary['max_y']

def entity_outside_boundary(entity):
    if entity.dxftype() == 'LINE':
        return not (is_inside_switzerland_boundary(entity.dxf.start) and is_inside_switzerland_boundary(entity.dxf.end))
    elif entity.dxftype() == 'LWPOLYLINE':
        return any(not is_inside_switzerland_boundary(point) for point in entity.get_points())
    elif entity.dxftype() == 'CIRCLE' or entity.dxftype() == 'ARC':
        return not is_inside_switzerland_boundary(entity.dxf.center)
    elif entity.dxftype() == 'ELLIPSE':
        return not is_inside_switzerland_boundary(entity.dxf.center)
    elif entity.dxftype() == 'SPLINE':
        return any(not is_inside_switzerland_boundary(point) for point in entity.fit_points())
    elif entity.dxftype() == 'TEXT' or entity.dxftype() == 'MTEXT':
        return not is_inside_switzerland_boundary(entity.dxf.insert)
    else:
        return False

def delete_entities_outside_boundary(doc):
    msp = doc.modelspace()

    entities_to_delete = []
    for entity in msp:
        if entity.dxftype() in ['LINE', 'LWPOLYLINE', 'CIRCLE', 'ARC', 'ELLIPSE', 'SPLINE', 'TEXT', 'MTEXT']:
            if entity_outside_boundary(entity):
                entities_to_delete.append(entity)

    for entity in entities_to_delete:
        msp.delete_entity(entity)

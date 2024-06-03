import ezdxf

def delete_all_point_entities(doc):
    msp = doc.modelspace()
    # Iterate over all POINT entities and remove them
    for point in msp.query('POINT'):
        msp.delete_entity(point)

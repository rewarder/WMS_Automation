import ezdxf
import os

def delete_entities_by_type(doc, entity_type):
    """
    Deletes entities of a specific type from the DXF document's modelspace.

    Args:
    - doc: The ezdxf document object.
    - entity_type: The entity type as a string to be deleted.
    """
    modelspace = doc.modelspace()
    entities_to_delete = [entity for entity in modelspace if entity.dxftype() == entity_type]
    for entity in entities_to_delete:
        modelspace.delete_entity(entity)

# Delete all 3DSolid entities
def delete_3dsolid_entities(doc):
    modelspace = doc.modelspace()
    threeDsolids = list(modelspace.query('3DSOLID'))
    for threeDsolid in threeDsolids:
        modelspace.delete_entity(threeDsolid)

# Delete all Solid entities
def delete_solid_entities(doc):
    modelspace = doc.modelspace()
    solids = list(modelspace.query('SOLID'))
    for solid in solids:
        modelspace.delete_entity(solid)

# Delete all Body entities
def delete_body_entities(doc):
    modelspace = doc.modelspace()
    bodies = list(modelspace.query('BODY'))
    for body in bodies:
        modelspace.delete_entity(body)

# Delete all Image entities
def delete_image_entities(doc):
    modelspace = doc.modelspace()
    images = list(modelspace.query('IMAGE'))
    for image in images:
        modelspace.delete_entity(image)

# Delete all WIPEOUT entities
def delete_wipeout_entities(doc):
    modelspace = doc.modelspace()
    wipeouts = list(modelspace.query('WIPEOUT'))
    for wipeout in wipeouts:
        modelspace.delete_entity(wipeout)

# Delete all Hatch entities
def delete_hatch_entities(doc):
    modelspace = doc.modelspace()
    hatches = list(modelspace.query('HATCH'))
    for hatch in hatches:
        modelspace.delete_entity(hatch)

# Delete all Point entities
def delete_point_entities(doc):
    modelspace = doc.modelspace()
    points = list(modelspace.query('POINT'))
    for point in points:
        modelspace.delete_entity(point)

# Delete all Text entities
def delete_text_entities(doc):
    modelspace = doc.modelspace()
    texts = list(modelspace.query('TEXT'))
    for text in texts:
        modelspace.delete_entity(text)

# Delete all MText entities
def delete_mtext_entities(doc):
    modelspace = doc.modelspace()
    mtexts = list(modelspace.query('MTEXT'))
    for mtext in mtexts:
        modelspace.delete_entity(mtext)

# Example usage:
# delete_body_entities('your_input_file.dxf', 'your_output_file.dxf')
# delete_image_entities('your_input_file.dxf', 'your_output_file.dxf')
# delete_wipeout_entities('your_input_file.dxf', 'your_output_file.dxf')
# ...

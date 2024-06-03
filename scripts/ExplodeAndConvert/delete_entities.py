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

# Delete all Body entities
def delete_body_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'BODY')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

# Delete all Image entities
def delete_image_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'IMAGE')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

# Delete all WIPEOUT entities
def delete_wipeout_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'WIPEOUT')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

# Delete all Hatch entities
def delete_hatch_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'HATCH')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

# Delete all Point entities
def delete_point_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'POINT')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

# Delete all Text entities
def delete_text_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'TEXT')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

# Delete all MText entities
def delete_mtext_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'MTEXT')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)


# Example usage:
# delete_body_entities('your_input_file.dxf', 'your_output_file.dxf')
# delete_image_entities('your_input_file.dxf', 'your_output_file.dxf')
# delete_wipeout_entities('your_input_file.dxf', 'your_output_file.dxf')

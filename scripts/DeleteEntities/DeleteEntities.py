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

def delete_all_insert_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'INSERT')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

def delete_all_body_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'BODY')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

def delete_all_image_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'IMAGE')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

def delete_wipeout_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'WIPEOUT')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

def delete_hatches_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'HATCH')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

def delete_points_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'POINT')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

def delete_texts_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'TEXT')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)

def delete_mtexts_entities(dxf_file_path, save_to=None):
    doc = ezdxf.readfile(dxf_file_path)
    delete_entities_by_type(doc, 'MTEXT')
    save_path = save_to or dxf_file_path
    doc.saveas(save_path)


# Example usage:
# delete_all_body_entities('your_input_file.dxf', 'your_output_file.dxf')
# delete_all_image_entities('your_input_file.dxf', 'your_output_file.dxf')
# delete_wipeout_entities('your_input_file.dxf', 'your_output_file.dxf')

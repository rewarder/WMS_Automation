import ezdxf

def copy_entities_into_new_drawing(doc):
    # Create a new in-memory drawing
    doc = ezdxf.new()
    # Get the model space from the new document
    new_model_space = doc.modelspace()

    # Iterate through all entities in the original document
    for entity in doc.modelspace():  # Access model space directly from 'doc'
        if entity.dxftype() in ('LINE', 'CIRCLE', 'ARC'):
            # Copy the entity to the new document with its properties
            new_entity = new_model_space.add_entity(entity)
            # Copy properties from the original entity to the new entity
            #for attr in entity.attribs:
            #    setattr(new_entity, attr, getattr(entity, attr))

    # Return the modified document
    return doc

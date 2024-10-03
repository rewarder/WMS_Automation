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
            new_entity = new_model_space.add_entity(entity.dxftype(), entity.dxf)
            # Optionally copy properties from the original entity to the new entity
            for attr in entity.attribs:
                 setattr(new_entity, attr, getattr(entity, attr))

    # Return the modified document
    return doc

def clean_drawing(doc):
    # Get the model space from the original document
    model_space = doc.modelspace()
    # Collect entities to delete
    entities_to_delete = []
    
    # Identify entities to delete
    for entity in model_space:
        if entity.dxftype() not in ('LINE', 'CIRCLE', 'ARC'):
            entities_to_delete.append(entity)

    # Delete the collected entities
    for entity in entities_to_delete:
        model_space.delete_entity(entity)

    return doc

# entity_counter.py
import ezdxf

def count_entities(doc):
    # Access the modelspace
    msp = doc.modelspace()

    # Dictionary to hold entity counts
    entity_counts = {}

    # Iterate through all entities in the modelspace
    for entity in msp:
        # Get the DXF type of the entity
        dxf_type = entity.dxftype()
        # Count the entities by their type
        entity_counts[dxf_type] = entity_counts.get(dxf_type, 0) + 1

    return entity_counts

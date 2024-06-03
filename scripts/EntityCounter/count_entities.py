import ezdxf
import sys

def count_entities(input_file):
    # Load the DXF document
    try:
        doc = ezdxf.readfile(input_file)
    except IOError:
        print(f'Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f'Invalid or corrupted DXF file.')
        sys.exit(2)

    # Access the modelspace
    msp = doc.modelspace()

    # Dictionary to hold entity counts
    entity_counts = {}

    # Iterate through all entities in the modelspace
    for entity in msp:
        # Get the DXF type of the entity
        dxf_type = entity.dxftype()
        # Count the entities by their type
        if dxf_type in entity_counts:
            entity_counts[dxf_type] += 1
        else:
            entity_counts[dxf_type] = 1

    return entity_counts

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python count_entities.py <input_dxf_file>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    entity_counts = count_entities(input_file_path)

    # Print the count of each entity type
    for entity_type, count in entity_counts.items():
        print(f"{entity_type}: {count}")

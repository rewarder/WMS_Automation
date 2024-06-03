import ezdxf
from ezdxf.math import Matrix44
import math

def explode_dimension(dim, modelspace):
    # Get all entities associated with the dimension
    entities = dim.virtual_entities()
    
    # Copy and transform each entity and add it to the modelspace
    for entity in entities:
        copied_entity = entity.copy()
        modelspace.add_entity(copied_entity)
    
    # Delete the original dimension
    modelspace.delete_entity(dim)

# Load the DXF document
doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Dimensions/Text.dxf")

# Access modelspace
modelspace = doc.modelspace()

# Explode all dimensions
dimensions = list(modelspace.query('DIMENSION'))  # Find all dimension entities in the modelspace
for dim in dimensions:
    explode_dimension(dim, modelspace)

# Save the modified DXF document
doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Dimensions/exploded_dimensions.dxf")

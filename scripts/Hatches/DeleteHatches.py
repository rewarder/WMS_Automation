import ezdxf

def delete_hatches(doc):
    modelspace = doc.modelspace()
    
    # Find all hatch entities in the modelspace
    hatches = list(modelspace.query('HATCH'))
    
    # Delete all hatch entities
    for hatch in hatches:
        modelspace.delete_entity(hatch)

# Load the DXF document
doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Hatches/Text.dxf")

# Delete all hatches
delete_hatches(doc)

# Save the modified DXF document
doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Hatches/Text_without_hatches.dxf")

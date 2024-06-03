import ezdxf

def delete_hatches(doc):
    modelspace = doc.modelspace()
    
    hatches = list(modelspace.query('HATCH'))
    for hatch in hatches:
        modelspace.delete_entity(hatch)

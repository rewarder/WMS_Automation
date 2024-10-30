import ezdxf

def remove_all_layouts_except_modelspace(doc):
    # Get all layout names
    layout_names = doc.layouts.names()

    # Iterate over all layouts and clear entities
    for layout_name in layout_names:
        if layout_name != 'Model':
            layout = doc.layouts.get(layout_name)
            layout.delete_all_entities()
            print(f'Cleared all entities in layout: {layout_name}')

    # Iterate and delete all but one paperspace layout
    for layout_name in layout_names:
        if layout_name != 'Model' and layout_name != 'Layout1':
            doc.layouts.delete(layout_name)
            print(f'Deleted layout: {layout_name}')
    
    # Return the modified document
    return doc
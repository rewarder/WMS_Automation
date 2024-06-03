import ezdxf

# Load an existing DXF document.
doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Test/wellThen.dxf")

# Make sure you're using the correct layout here. 
# For modelspace use doc.modelspace()
# For a specific paperspace layout use doc.layout('LayoutName')
msp = doc.modelspace()

# Iterate through all entities in the model space and find text entities
for entity in msp:
    if entity.dxftype() == 'TEXT':
        # Retrieve the text entity's bounding box
        # The dxfattribs method gives you access to the common DXF attributes
        text_content = entity.dxfattribs().get('text')
        insert_point = entity.dxfattribs().get('insert')
        height = entity.dxfattribs().get('height')
        width = entity.dxfattribs().get('width')  # This requires the 'ezdxf' v0.16 or later
        
        # Print out the text and its bounding box size
        print(f"Text: {text_content}")
        print(f"Insertion Point: {insert_point}")
        print(f"Height: {height}")
        print(f"Width: {width}")

        # If you want to consider the rotation and calculate the actual bounding box considering all 4 points
        # You will need additional calculations based on the rotation angle,
        # which is beyond the scope of this simple example.

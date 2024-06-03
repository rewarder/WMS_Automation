import ezdxf

# Load the DXF document
doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Test/wellThen.dxf")

# Access the modelspace where the entities are stored
msp = doc.modelspace()

# Iterate through all TEXT entities and print their insertion points
for text in msp.query('TEXT'):
    # The position attribute contains the insertion point of the TEXT entity
    insertion_point = text.dxf.insert
    print(f"TEXT entity at insertion point: {insertion_point}")

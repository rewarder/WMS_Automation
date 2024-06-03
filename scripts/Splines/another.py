import ezdxf
from ezdxf.math import ConstructionPolyline

# Read the DXF file
doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Splines/modified_GD1_ELE_RUB_Ausführung GD1 7.OG 50__GEOREF.dxf")
msp = doc.modelspace()

# Query all SPLINE entities in the model space
splines = msp.query("SPLINE")

# Convert each spline to a polyline
for spline in splines:
    # Create a ConstructionPolyline from the spline's flattened points
    polyline_points = spline.flattening(0.01)
    polyline = ConstructionPolyline(polyline_points)
    
    # Create a new LWPOLYLINE entity in the model space
    msp.add_lwpolyline(polyline_points, close=False)
    
    # Get dividing points with a distance of 1.0 drawing unit to each other
    points = list(polyline.divide_by_length(1.0))

# Save the modified DXF file
doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Splines/converted_modified_GD1_ELE_RUB_Ausführung GD1 7.OG 50__GEOREF.dxf")

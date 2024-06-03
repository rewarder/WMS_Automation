import ezdxf
from ezdxf.math import ConstructionPolyline

doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Splines/modified_GD1_ELE_RUB_Ausführung GD1 7.OG 50__GEOREF.dxf")
msp = doc.modelspace()
splines = msp.query("SPLINE")
for spline in splines:
    polyline = ConstructionPolyline(spline.flattening(0.01))
    print(f"Entity {spline} has an approximated length of {polyline.length}")
    # get dividing points with a distance of 1.0 drawing unit to each other
    points = list(polyline.divide_by_length(1.0))

doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Splines/converted_modified_GD1_ELE_RUB_Ausführung GD1 7.OG 50__GEOREF.dxf")

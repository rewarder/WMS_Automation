import ezdxf
from ezdxf.math import ConstructionPolyline

def convert_splines_to_polylines(input_dxf_path, output_dxf_path, flattening_distance=0.01):
    # Read the DXF file
    doc = ezdxf.readfile(input_dxf_path)
    msp = doc.modelspace()

    # Query all SPLINE entities in the model space
    splines = msp.query("SPLINE")

    # Convert each SPLINE to a POLYLINE
    for spline in splines:
        # Flatten the spline to a series of points
        polyline_points = spline.flattening(flattening_distance)
        
        # Create a new LWPOLYLINE entity in the model space
        polyline = msp.add_lwpolyline(polyline_points, close=False)
        
        # Copy attributes from the spline to the polyline
        polyline.dxf.layer = spline.dxf.layer
        polyline.dxf.color = spline.dxf.color
        polyline.dxf.linetype = spline.dxf.linetype
        polyline.dxf.lineweight = spline.dxf.lineweight
        polyline.dxf.ltscale = spline.dxf.ltscale

        # Delete the original spline
        msp.delete_entity(spline)

        # Convert the polyline to individual lines
        vertices = list(polyline.vertices())
        for i in range(len(vertices) - 1):
            start_point = vertices[i]
            end_point = vertices[i + 1]

            line = msp.add_line(start_point, end_point)
            
            # Copy attributes from the polyline to the line
            line.dxf.layer = polyline.dxf.layer
            line.dxf.color = polyline.dxf.color
            line.dxf.linetype = polyline.dxf.linetype
            line.dxf.lineweight = polyline.dxf.lineweight
            line.dxf.ltscale = polyline.dxf.ltscale

        # Delete the polyline after converting to lines
        msp.delete_entity(polyline)

    # Save the modified DXF file
    doc.saveas(output_dxf_path)

if __name__ == "__main__":
    input_dxf_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Splines/modified_GD1_ELE_RUB_Ausführung GD1 7.OG 50__GEOREF.dxf"
    output_dxf_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Splines/converted_modified_GD1_ELE_RUB_Ausführung GD1 7.OG 50__GEOREF.dxf"
    convert_splines_to_polylines(input_dxf_path, output_dxf_path)
    print(f"Converted splines to polylines and saved to {output_dxf_path}")

import ezdxf

def create_2d_line_dxf(output_file, start_point, end_point):
    # Create a new DXF document
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()
    
    # Add a 2D line to the modelspace
    msp.add_line(start_point, end_point)
    
    # Save the DXF document
    doc.saveas(output_file)

# Example usage
output_dxf = 'C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/SimpleDXFentities/output_2d_line.dxf'
start_point_2d = (10, 20)  # X, Y coordinates only
end_point_2d = (30, 40)    # X, Y coordinates only
create_2d_line_dxf(output_dxf, start_point_2d, end_point_2d)

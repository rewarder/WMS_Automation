import ezdxf

def convert_linestringz_to_linestring(dxf_file, output_file):
    # Open the DXF file
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()

    # Iterate through all entities in the modelspace
    for entity in list(msp):
        if entity.dxftype() == 'POLYLINE' and entity.is_3d_polyline:
            # Extract 3D vertices
            vertices_3d = [(v.dxf.x, v.dxf.y) for v in entity.vertices]
            
            # Create a new 2D polyline (LineString)
            new_polyline = msp.add_lwpolyline(vertices_3d)
            
            # Copy properties from the original polyline to the new polyline
            new_polyline.dxf.color = entity.dxf.color
            new_polyline.dxf.layer = entity.dxf.layer
            new_polyline.dxf.linetype = entity.dxf.linetype
        
            # Delete the original 3D polyline
            msp.delete_entity(entity)
        elif entity.dxftype() == 'LINE':
            # Extract start and end points
            start_point_2d = (entity.dxf.start.x, entity.dxf.start.y)
            end_point_2d = (entity.dxf.end.x, entity.dxf.end.y)
            
            # Create a new 2D line
            new_line = msp.add_line(start_point_2d, end_point_2d)
            
            # Copy properties from the original line to the new line
            new_line.dxf.color = entity.dxf.color
            new_line.dxf.layer = entity.dxf.layer
            new_line.dxf.linetype = entity.dxf.linetype
            
            # Delete the original 3D line
            msp.delete_entity(entity)
    
    # Save the modified DXF file
    doc.saveas(output_file)

# Example usage
input_dxf = 'C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/SimpleDXFentities/input.dxf'
output_dxf = 'C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/SimpleDXFentities/output.dxf'
convert_linestringz_to_linestring(input_dxf, output_dxf)

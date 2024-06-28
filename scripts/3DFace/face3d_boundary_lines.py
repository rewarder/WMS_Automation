import ezdxf
import os

def create_boundary_lines(doc):
    # Get the modelspace of the document
    msp = doc.modelspace()
    
    # Iterate through all Face3D entities in the modelspace
    for face3d in msp.query('3DFACE'):
        # Get the vertices of the Face3D entity
        vertices = face3d.wcs_vertices()
        
        # Get the layer of the current Face3D entity
        layer = face3d.dxf.layer
        
        # Create lines for each edge of the Face3D and place them on the same layer
        for i in range(len(vertices)):
            start_point = vertices[i]
            end_point = vertices[(i + 1) % len(vertices)]
            msp.add_line(start=start_point, end=end_point, dxfattribs={'layer': layer})

def main():
    # Hard-coded input file path
    input_file = 'C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/3DFace/1981_Grenzacherstrasse_best_Bruecke.dxf'
    
    # Load the input DXF document
    doc = ezdxf.readfile(input_file)
    
    # Create boundary lines for all Face3D entities
    create_boundary_lines(doc)
    
    # Save the modified document
    output_file = os.path.splitext(input_file)[0] + '_with_boundaries.dxf'
    doc.saveas(output_file)
    print(f"DXF file saved as '{output_file}'")

if __name__ == "__main__":
    main()

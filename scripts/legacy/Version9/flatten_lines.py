import ezdxf

def flatten3d_lines(doc):

    # Create a new DXF document for 2D coordinates
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # Iterate through entities to extract 3D coordinates and convert to 2D
    for entity in msp:
        if entity.dxftype() == 'LINE':
            start_xyz = entity.dxf.start
            end_xyz = entity.dxf.end

            # Convert 3D to 2D by ignoring the z-coordinate
            start_2d = (start_xyz.x, start_xyz.y)
            end_2d = (end_xyz.x, end_xyz.y)

            # Add the 2D line to the new document
            msp.add_line(start_2d, end_2d)

    return doc

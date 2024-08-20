import ezdxf

def get_ellipse_details(ellipse):
    major_axis_vector = ellipse.dxf.major_axis
    center = ellipse.dxf.center
    extrusion = ellipse.dxf.extrusion
    start_param = ellipse.dxf.start_param
    end_param = ellipse.dxf.end_param
    return major_axis_vector, center, extrusion, start_param, end_param

def print_ellipse_details(dxf_file_path):
    try:
        # Load the DXF document
        doc = ezdxf.readfile(dxf_file_path)
        msp = doc.modelspace()

        # Iterate over all the ellipses in the modelspace
        for entity in msp.query('ELLIPSE'):
            major_axis_vector, center, extrusion, start_param, end_param = get_ellipse_details(entity)
            rounded_major_axis_vector = tuple(round(coord, 3) for coord in major_axis_vector)

            print(f"Ellipse details:")
            print(f"  Major axis vector: {rounded_major_axis_vector}")
            print(f"  Center: {center}")
            print(f"  Extrusion: {extrusion}")
            print(f"  Start parameter: {start_param}")
            print(f"  End parameter: {end_param}")

    except IOError:
        print(f"Could not read file: {dxf_file_path}")
    except ezdxf.DXFStructureError:
        print(f"Invalid DXF file: {dxf_file_path}")

# Example usage
dxf_file_path = 'ellipse.dxf'
print_ellipse_details(dxf_file_path)

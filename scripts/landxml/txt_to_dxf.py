import ezdxf

def read_coordinates_from_txt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    coordinates = []
    for line in lines:
        # Split the line by commas and convert to float
        x, y, z = map(float, line.strip().split(','))
        coordinates.append((x, y, z))
    
    return coordinates

def write_points_to_dxf(coordinates, dxf_file_path):
    # Create a new DXF document
    doc = ezdxf.new()
    msp = doc.modelspace()
    
    # Add points to the DXF model space
    for (x, y, z) in coordinates:
        msp.add_point((x, y, z))
    
    # Save the DXF document
    doc.saveas(dxf_file_path)

def main():
    input_txt_file = 'points_output_02.txt'  # Change this to your input file path
    output_dxf_file = 'output_02.dxf'      # Change this to your desired output file path
    
    coordinates = read_coordinates_from_txt(input_txt_file)
    write_points_to_dxf(coordinates, output_dxf_file)
    print(f"DXF file created: {output_dxf_file}")

if __name__ == "__main__":
    main()

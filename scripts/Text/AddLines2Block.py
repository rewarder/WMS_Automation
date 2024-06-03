import ezdxf

def create_block_from_lines(filepath, block_name):
  try:
    doc = ezdxf.readfile(filepath)
    msp = doc.modelspace()  # Get the modelspace

    lines = msp.query("LINE")
    block = doc.blocks.new(block_name)

    for line in lines:
        start_point = (line.dxf.start.x, line.dxf.start.y, line.dxf.start.z)
        end_point = (line.dxf.end.x, line.dxf.end.y, line.dxf.end.z)

        new_line = block.add_line(start=start_point, end=end_point)

        doc.saveas("output.dxf")
    print(f"Block '{block_name}' created containing all lines from the DXF file. Saved as 'output.dxf'.")

  except Exception as e:
    print(f"Error processing file: {filepath}")
    print(f"Error message: {e}")

# Example usage
filepath = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Text/Text2Lines_PreservedHeight.dxf"  # Replace with your actual DXF file path
block_name = "AllLinesBlock"

create_block_from_lines(filepath, block_name)

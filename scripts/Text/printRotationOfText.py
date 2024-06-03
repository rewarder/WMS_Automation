import ezdxf

def extract_text_rotations(input_file):
  """
  Extracts and prints the rotation of each text entity in the input DXF file.

  Args:
      input_file: The path to the input DXF file.
  """

  # Read the DXF file
  doc = ezdxf.readfile(input_file)

  # Get the text entities from the model space
  msp = doc.modelspace()
  text_entities = msp.query("TEXT")

  # Iterate through text entities and print their rotation
  for text_entity in text_entities:
    rotation = text_entity.dxf.rotation  # Assuming rotation is stored in dxf.rotation attribute
    print(f"Text Entity Rotation: {rotation:.2f} degrees")  # Format with 2 decimal places

if __name__ == "__main__":
  # Specify the input DXF file path
  input_dxf_file = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Text/Text.dxf"

  # Extract and print text rotations
  extract_text_rotations(input_dxf_file)

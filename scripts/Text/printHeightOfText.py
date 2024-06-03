import ezdxf

def extract_text_heights(input_file):
  """
  Extracts and prints the height of each text entity in the input DXF file.

  Args:
      input_file: The path to the input DXF file.
  """

  # Read the DXF file
  doc = ezdxf.readfile(input_file)

  # Get the text entities from the model space
  msp = doc.modelspace()
  text_entities = msp.query("TEXT")

  # Iterate through text entities and print their heights
  for text_entity in text_entities:
    height = text_entity.dxf.height
    print(f"Text Entity Height: {height}")

if __name__ == "__main__":
  # Specify the input DXF file path
  input_dxf_file = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Text/Text.dxf"

  # Extract and print text heights
  extract_text_heights(input_dxf_file)

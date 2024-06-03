import ezdxf
import os
import shutil  # Import shutil for file operations (renaming, deleting)

# Get input file path from command-line argument
input_file = sys.argv[1]

# Extract directory and filename
input_dir, input_filename = os.path.split(input_file)
file_extension = os.path.splitext(input_filename)[1].lower()  # Get lowercase extension

# Generate temporary file path within the same directory
temp_file = os.path.join(input_dir, f"temp_{input_filename}")

# Open the DXF/DWG document (handle both extensions)
if file_extension == ".dxf":
    doc = ezdxf.readfile(input_file)
elif file_extension == ".dwg":
    doc = ezdxf.readdwg(input_file)
else:
    print(f"Error: Unsupported file format. Please provide a DXF or DWG file.")
    exit(1)










# Add actual SCRIPT











# Save the modified DXF/DWG file to the temporary file
doc.saveas(temp_file)

# Delete the original file (optional - create a backup if needed)
# os.remove(input_file)

# Rename the temporary file to the desired output filename
new_filename = f"modified_{input_filename}"
output_file = os.path.join(input_dir, new_filename)
shutil.move(temp_file, output_file)

print(f"DXF/DWG file successfully modified and saved to: {output_file}")

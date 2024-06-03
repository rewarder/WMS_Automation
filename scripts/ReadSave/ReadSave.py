import ezdxf
from ezdxf.addons import odafc

# Option 1: Absolute file path (replace with the actual location of your file)
filepath = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/221019_Kanalisation.dwg"
doc = odafc.readfile(filepath)

# Option 2: Relative file path (assuming the DWG file is in the same folder as the script)
# filepath = "221019_Kanalisation.dwg"  # Uncomment for relative path
# doc = odafc.readfile(filepath)

# Export document as DWG file for AutoCAD R2018 (assuming successful reading)
odafc.export_dwg(doc, '221019_Kanalisation_converted.dwg', version='R2018')

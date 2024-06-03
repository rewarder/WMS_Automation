import pathlib
import ezdxf
from ezdxf.addons.drawing import Properties, Frontend, RenderContext
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.tools import fonts
from ezdxf import zoom

CWD = pathlib.Path("~/Desktop/Outbox").expanduser()
if not CWD.exists():
    CWD = pathlib.Path(".")

# Ensure your SHX font files are in a directory that ezdxf can find
fonts.add_font_paths('C:/Program Files/Autodesk/AutoCAD 2022/Fonts')

def render_txt(fontname: str, text: str) -> ezdxf.document.Drawing:
    doc = ezdxf.new()
    msp = doc.modelspace()
    
    # Ensure the font (SHX file) is registered in the font cache
    font = fonts.load(fontname)
    if not font:
        print(f"Could not load font: {fontname}")
        return doc
    
    # The style must be defined in the document with a unique name
    if fontname not in doc.styles:
        doc.styles.new(fontname, dxfattribs={'font': fontname})
    
    # Add the text with the specified SHX font
    msp.add_text(
        text,
        dxfattribs={
            'style': fontname,
        })

    return doc

doc = render_txt("iso.shx", "7410/A")
zoom.extents(doc.modelspace())
doc.saveas(CWD / "iso_shx.dxf")

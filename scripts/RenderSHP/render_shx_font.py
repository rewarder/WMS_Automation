import ezdxf
from ezdxf import path, zoom
from ezdxf.fonts import fonts
from ezdxf.document import Drawing

ezdxf.options.support_dirs = ["C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/dxfsupport"]

fonts.build_system_font_cache()

def render_txt(fontname: str, text: str) -> Drawing:
    doc = ezdxf.new()
    msp = doc.modelspace()
    font = fonts.make_font(fontname, cap_height=3.5)
    text_path = font.text_path(text)
    # convert the optimized 2D text_path to a regular Path()
    path.render_splines_and_polylines(msp, [text_path.to_path()])
    return doc


doc = render_txt("iso.shx", "7410/A")
zoom.extents(doc.modelspace())
doc.saveas("iso_shx.dxf")
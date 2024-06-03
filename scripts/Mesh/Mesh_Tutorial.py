import ezdxf
from ezdxf import colors
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.render import forms

cube = forms.cube().scale_uniform(10).subdivide(2)
red = GfxAttribs(color=colors.RED)
green = GfxAttribs(color=colors.GREEN)
blue = GfxAttribs(color=colors.BLUE)

doc = ezdxf.new()
msp = doc.modelspace()

# render as MESH entity
cube.render_mesh(msp, dxfattribs=red)
cube.translate(20)

doc.saveas("mesh.dxf")
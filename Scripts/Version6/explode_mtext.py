import ezdxf
from ezdxf.addons import MTextExplode

def explode_mtext(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    msp = doc.modelspace()
    with MTextExplode(msp) as xpl:
        for mtext in msp.query("MTEXT"):
            xpl.explode(mtext)
    doc.saveas(output_file)

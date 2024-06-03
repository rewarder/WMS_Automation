import ezdxf
from ezdxf.math import Matrix44
import math

def explode_blocks(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    modelspace = doc.modelspace()

    def explode_block_reference(block_ref, modelspace):
        block_definition = block_ref.block()
        m = Matrix44.chain(
            Matrix44.translate(block_ref.dxf.insert.x, block_ref.dxf.insert.y, block_ref.dxf.insert.z),
            Matrix44.z_rotate(math.radians(block_ref.dxf.rotation)),
            Matrix44.scale(block_ref.dxf.xscale, block_ref.dxf.yscale, block_ref.dxf.zscale)
        )
        for entity in block_definition:
            if entity.dxf.layer in modelspace.doc.layers and modelspace.doc.layers.get(entity.dxf.layer).is_frozen():
                continue
            if entity.dxf.layer in modelspace.doc.layers and not modelspace.doc.layers.get(entity.dxf.layer).is_on():
                continue
            copied_entity = entity.copy()
            if 'AcDbEntity' in copied_entity.dxftype():
                copied_entity.transform(m)
            modelspace.add_entity(copied_entity)
        modelspace.delete_entity(block_ref)

    block_refs = list(modelspace.query('INSERT'))
    for block_ref in block_refs:
        explode_block_reference(block_ref, modelspace)

    doc.saveas(output_file)

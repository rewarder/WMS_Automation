import ezdxf

def explode_dimensions(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    modelspace = doc.modelspace()

    def explode_dimension(dim, modelspace):
        entities = dim.virtual_entities()
        for entity in entities:
            copied_entity = entity.copy()
            modelspace.add_entity(copied_entity)
        modelspace.delete_entity(dim)

    dimensions = list(modelspace.query('DIMENSION'))
    for dim in dimensions:
        explode_dimension(dim, modelspace)

    doc.saveas(output_file)

import ezdxf

def delete_all_text_entities(doc):
    msp = doc.modelspace()
    # Iterate over all TEXT and MTEXT entities and remove them
    for text in msp.query('TEXT'):
        msp.delete_entity(text)
    for mtext in msp.query('MTEXT'):
        msp.delete_entity(mtext)

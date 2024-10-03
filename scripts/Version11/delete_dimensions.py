import ezdxf

def delete_dimension_styles(doc):
    """Remove all dimension styles from the given DXF document."""
    try:
        # Access the dimension styles
        dim_styles = doc.dimstyles

        # Remove all dimension styles
        for dim_style_name in list(dim_styles):
            if isinstance(dim_style_name, str):  # Ensure the name is a string
                dim_styles.remove(dim_style_name)

        return doc

    except Exception as e:
        print(f"Error while deleting dimension styles: {e}")
        return None
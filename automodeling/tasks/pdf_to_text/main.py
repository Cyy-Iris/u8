import pdftotext

def pdf_to_text(fpath: str) -> list:
    """Extract text from a PDF file.

    Extract the text from a PDF file using the pdftotext library,
    returning a JSON with an array of pages.

    Args:
        fpath: path to the PDF file

    Returns:
        An array of text representing the pages of the PDF file encoded 
        as a JSON string
    """
    with open(fpath, "rb") as f:
        pdf = pdftotext.PDF(f, physical=True)

    full_pdf = []
    for page in pdf:
        full_pdf.append(page)

    return full_pdf
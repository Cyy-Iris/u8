'''
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
'''

from langchain.document_loaders import PyPDFLoader
from task_logic.pdf_to_md.utils import (
    remove_pages,
    merge_pages,
    POST_PROCESSING_STEPS,
)


def pdf_to_md(fpath: str) -> str:
    loader = PyPDFLoader(fpath)
    pages = loader.load_and_split()
    pages = remove_pages(pages)
    md = merge_pages(pages)
    for post_processing_step in POST_PROCESSING_STEPS:
        md = post_processing_step(md)

    return md

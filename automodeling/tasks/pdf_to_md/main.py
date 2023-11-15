from typing import List

from langchain.document_loaders import PyPDFLoader

from automodeling.tasks.pdf_to_md.utils import POST_PROCESSING_STEPS, remove_pages


def pdf_to_md(fpath: str) -> List[str]:
    loader = PyPDFLoader(fpath)
    pages = loader.load_and_split()
    pages = remove_pages(pages)
    page_mds: List[str] = []
    for md in pages:
        page_md = md.page_content
        for post_processing_step in POST_PROCESSING_STEPS:
            page_md = post_processing_step(page_md)
        page_mds.append(page_md)

    return page_mds

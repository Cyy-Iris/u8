from typing import Callable, List

from langchain.schema.document import Document


def merge_pages(pages: List[Document]) -> str:
    return "\n".join([p.page_content for p in pages])


def remove_page_nums(md: str) -> str:
    lines = md.split("\n")
    new_lines = []

    last_page_number = None

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.isdigit():
            if (last_page_number is None and int(stripped_line) in {1, 2}) or (
                last_page_number is not None
                and int(stripped_line) == last_page_number + 1
            ):
                last_page_number = int(stripped_line)
                continue

        new_lines.append(line)

    return "\n".join(new_lines)


def remove_pages(pages: List[Document]) -> List[Document]:
    has_content = ["content" in p.page_content.lower() for p in pages[:3]]
    if has_content == [False, True, False]:
        pages = pages[1:]

    return pages


POST_PROCESSING_STEPS: List[Callable] = [remove_page_nums]

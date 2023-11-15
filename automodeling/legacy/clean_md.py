from llama_index.llms import ChatMessage

PROMPT = """Transform the users input representing a page extracted from PDF into a correct markdown, identifying the headings and remove the pages header and footers. Do not invent text. Do not use bold and italic to denote title, instead use # notation with as many '#' as needed. In case of alpha numerical list do not use the list notation. Instead create title "List item X" using the appropriate number of #. Please make sure to continue on previous page markdown when available in the conversation and to include all the relevant text from the content. Please respect the hierarchy found in the currently extracted table of content as follows
---
TABLE OF CONTENTS
{}
---"""


def clean_page(page, toc, llm):
    clean_page = llm.chat(
        [
            ChatMessage(role="system", content=PROMPT.format(toc)),
            ChatMessage(role="user", content=page),
        ],
    ).message.content
    return clean_page

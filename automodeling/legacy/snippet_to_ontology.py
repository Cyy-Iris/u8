import json
from llama_index.llms import ChatMessage

EXAMPLE_1 = {
    "word": "You",
    "definition": "You means policyholder",
    "scope": "Section A",
}
EXAMPLE_1 = json.dumps(EXAMPLE_1)

EXAMPLE_2 = {
    "word": "Car",
    "definition": "A car is a vehicle with 4 wheels",
    "scope": "All sections of this policy",
}
EXAMPLE_2 = json.dumps(EXAMPLE_2)

EMPTY_STR = "none"


PROMPT = f"""Classify the users input representing an extract of text. \
    For every word that are explicitly 'defined' in this extract output them in the JSONL form:
{EXAMPLE_1}
{EXAMPLE_2}

The defined words need to be explicitly defined in the extract. For example:
"Foo" means ...
or contain in a Definition section
or preface by a text like the following word is defined as...

Always write a definition with the maximum amount of available detail without adding any details not present in the text.
If no definitions are found return the string "{EMPTY_STR}".
"""


def extract_ontology_from_next_snippet(snippet, llm):
    ontology = llm.chat(
        [
            ChatMessage(role="system", content=PROMPT),
            ChatMessage(role="user", content=snippet),
        ]
    ).message.content

    if ontology == EMPTY_STR:
        return None

    ontology_json = [
        json.loads(line.strip()) for line in ontology.split("\n") if line.strip()
    ]
    return ontology_json

from llama_index.llms import ChatMessage


EXAMPLE_1_INPUT = """CONTENTS
Motor Breakdown Insurance Policy & Summary
A – Policy wording 3
Breakdown Causes 8
SECTION A – AXA LOCAL 9
SECTION B – AXA NATIONWIDE 10
SECTION C – AXA NATIONWIDE & HOMESTART 11
SECTION A, B, C – MISFUELLING 12
SECTION D – AXA EUROPEAN 13
SECTION E – GENERAL EXCLUSIONS THAT APPLY TO ALL PARTS 17 OF THIS POLICY
SECTION F – GENERAL CONDITIONS APPLYING TO ALL PARTS 20 OF THIS POLICY
B – Policy summary 26 AXA BREAKDOWN COVER POLICY SUMMARY 26"""

EXAMPLE_1_OUTPUT = """
# A
## Policy wording
## Breakdown Causes
## SECTION A – AXA LOCAL
## SECTION B – AXA NATIONWIDE
## SECTION C – AXA NATIONWIDE & HOMESTART
## SECTION A, B, C – MISFUELLING
## SECTION D – AXA EUROPEAN
## SECTION E – GENERAL EXCLUSIONS
## SECTION F – GENERAL CONDITIONS
# B
## Policy summary AXA BREAKDOWN COVER POLICY SUMMARY
"""

_PROMPT = f"""Simplify the markdown table of contents provided by the user. \
    Keep the same hash based markdown formatting to denote the levels of hierarchy. \
        Do not add any extra information. Make sure every title from the input is represented in the output.

example input:
{EXAMPLE_1_INPUT}

example output:

{EXAMPLE_1_OUTPUT}"""


def simplify_table_of_contents(toc_page, llm):
    simplified_toc = llm.chat(
        [
            ChatMessage(role="system", content=_PROMPT),
            ChatMessage(role="user", content=toc_page),
        ],
    ).message.content
    return simplified_toc

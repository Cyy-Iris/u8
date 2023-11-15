import json
from llama_index.llms import ChatMessage


PROMPT = """`User will provide some logic samples. Your task is to convert it to json based on the examples.
Output only the JSON. Do not output non JSON content/text.
If a valid JSON cannot be generated, return { "ok": false }.
"""

EXAMPLE_1 = [
    ChatMessage(
        role="user",
        content="""(EVENT="Huricane" AND DAMAGE="Loss" AND (IMPACTED_OBJECT="House" OR IMPACTED_OBJECT="Car") AND SERVICE="Hotel night") THEN LIMIT{{amount:40, unit:eur, per:night}}""",
    ),
    ChatMessage(
        role="assistant",
        content=json.dumps(
            {
                "condition": {
                    "type": "operation",
                    "operator": "and",
                    "operands": [
                        {"type": "EVENT", "value": "Huricane"},
                        {"type": "DAMAGE", "value": "Loss"},
                        {
                            "type": "operation",
                            "operator": "or",
                            "operands": [
                                {"type": "IMPACTED_OBJECT", "value": "House"},
                                {"type": "operation", "operator": "and"},
                            ],
                            "operands": [
                                {"type": "IMPACTED_OBJECT", "value": "Car"},
                                {"type": "test", "value": "CAR_AGE>1"},
                            ],
                        },
                        {"type": "SERVICE", "value": "Hotel night"},
                    ],
                    "then": {
                        "type": "LIMIT",
                        "value": {"amount": 40, "unit": "eur", "per": "night"},
                    },
                }
            }
        ),
    ),
]

EXAMPLE_2 = [
    ChatMessage(
        role="user",
        content="""(NUMBER_OF_MISFUELING_CLAIMS <= 2) THEN COVER {for: "Misfuelling claims"}""",
    ),
    ChatMessage(
        role="assistant",
        content=json.dumps(
            {
                "condition": {
                    "type": "operation",
                    "operator": "and",
                    "operands": [
                        {"type": "test", "value": "NUMBER_OF_MISFUELING_CLAIMS<=2"}
                    ],
                    "then": {"type": "COVER", "value": {"for": "Misfuelling claims"}},
                }
            }
        ),
    ),
]


def convert_lap_to_json(lap, llm):
    lap_json = llm.chat(
        [ChatMessage(role="system", content=PROMPT)]
        + EXAMPLE_1
        + EXAMPLE_2
        + [ChatMessage(role="user", content=json.dumps(lap))]
    ).message.content
    lap_json = json.loads(lap_json)
    return lap_json

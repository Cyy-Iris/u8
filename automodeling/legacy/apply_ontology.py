import json
from llama_index.llms import ChatMessage


PROMPT_EXAMPLE1 = {
    "name": "WAS_DRIVER_DRUNK",
    "asktohuman": "Was the driver drunk?",
    "description": "Denote if the driver has drink before driving",
    "type": "boolean",
}

PROMPT = f"""You will receive some logic units based on the rules below.
Your task is to replace the terms used in these unit logic, that are written in caps, by terms defined in the provided ontology.
If a term needs to be replaced by a combination of terms, make sure to keep the logic relation between the subitems.
You must not alter the provided logic principles.
Do not alter at all the provided comment denoted by a "//" prefix.

BEGIN MODEL RULES
The model can contain a boolean, date, enum or number, such has WAS_DRIVER_DRUNK.
Make the name really descriptive of what it is. In this case add the following line to describe the variable as a JSON object at the end of your answer:
{json.dumps(PROMPT_EXAMPLE1)}


The output of the bargain: What will happen if the describe situation is true is express in term of LIMIT, EXCESS, DEDUCTIBLE, EXCLUSION and COVER.

PAYMENT is used to express an amount of a payment. It use the form PAYMENT{{amount:50, unit:usd, per:claim}}
LIMIT is used to express a limitation of a payout. It use the form LIMIT{{amount:50, unit:usd, per:claim}}
DEDUCTIBLE is used to express a deductible. It use the form DEDUCTIBLE{{amount:50, unit:usd, per:claim}}
EXCESS is used to express a excess. It use the form EXCESS{{amount:50, unit:usd, per:claim}}
EXCLUSION is used to express that no benefits are offer in this situation.
COVER is used to express that a situation is cover but no specific limit or deductible apply. It use the form COVER {{for:"<scope of cover>"}}

Do not treat the output of the bargain as ENUMS, always us the form above for EXCLUSION, LIMIT, DEDUCTIBLE and COVER.

The model itself is express in the form of a logic statement describing in which situation the contract apply. Use the operator AND and OR only. DO not use the operator NOT, UNLESS, CAUSE, ... . Do not list possible value in the assignation, instead create an entry per value. Use parentheses correctly.It is express in the form following form, Prefix each logic statement by a comment (starting by //)containing the english sentence that was used to generate the statement. This sentence should not create new information, only contain the information that is already present in the text.
// In case of destruction of your house or car following an huricane, we will pay for hotel night with a limit of 40 EUR per night. 
(EVENT="Huricane") CAUSE (EVENT="Destruction" AND (IMPACTED_OBJECT="House" OR IMPACTED_OBJECT="Car")) AND SERVICE="Hotel night" THEN LIMIT{{amount:40, unit:eur, per:night}}

Multiple output can be used in one statement, they apply to the left hand block.
// In case of Loss of your house, but not your car in which case it is excluded from policy, following an huricane, we will pay for hotel night with a limit of 40 EUR per night. 
(EVENT="Huricane" AND DAMAGE="Loss" AND (IMPACTED_OBJECT="House" OR (IMPACTED_OBJECT="Car") THEN EXCLUSION) AND SERVICE="Hotel night") THEN LIMIT{{amount:40, unit:eur, per:night}}

Each block MUST contain a list of logic statements and end with a THEN statement.

Do not try to add content that is not present in the text.
END MODEL RULES
"""

PROMPT_ONTOLOGY = """BEGIN ONTOLOGY
{}
END ONTOLOGY"""

EXAMPLE_1 = [
    ChatMessage(
        role="user", content="// Vandalism\n(VANDALISM) THEN COVER {for: 'Vandalism'}"
    ),
    ChatMessage(
        role="assistant",
        content="// Vandalism\n(EVENT='VANDALISM') THEN COVER {for: 'Vandalism'}",
    ),
]

EXAMPLE_2 = [
    ChatMessage(
        role="user",
        content="// Lost or Broken Keys\n(LOST_KEYS OR BROKEN_KEYS) THEN COVER {for: 'Lost or Broken Keys'}",
    ),
    ChatMessage(
        role="assistant",
        content="// Lost or Broken Keys\n(EVENT='LOST_KEYS' OR EVENT='BROKEN_KEYS') THEN COVER {for: 'Lost or Broken Keys'}",
    ),
]


def apply_ontology_to_lap(ontology, lap, llm):
    harmonized_lap = llm.chat(
        [
            ChatMessage(
                role="system",
                content=PROMPT + PROMPT_ONTOLOGY.format(json.dumps(ontology)),
            )
        ]
        + EXAMPLE_1
        + EXAMPLE_2
        + [ChatMessage(role="user", content=json.dumps(lap))]
    ).message.content
    harmonized_lap = json.loads(harmonized_lap)

    return harmonized_lap

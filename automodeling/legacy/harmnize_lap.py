import json
from llama_index.llms import ChatMessage


HARMONIZED_ONTOLOGY = [
    {
        "name": "TRIGGER_EVENT",
        "asktohuman": "What triggered the event?",
        "description": "Denote the initiating event or circumstance",
        "type": "enum",
        "options": [],
    },
    {
        "name": "EVENT",
        "asktohuman": "What was the event?",
        "description": "Specify the actual event or incident",
        "type": "enum",
        "options": [],
    },
    {
        "name": "DAMAGE",
        "asktohuman": "What damage was caused?",
        "description": "Specify the type or extent of damage",
        "type": "enum",
        "options": [],
    },
    {
        "name": "IMPACTED_OBJECT",
        "asktohuman": "What object was impacted?",
        "description": "Specify the object or item that sustained damage or was affected",
        "type": "enum",
        "options": [],
    },
    {
        "name": "SERVICE",
        "asktohuman": "What service is required?",
        "description": "Specify the kind of service or action needed post-event",
        "type": "enum",
        "options": [],
    },
]

HARMONIZED_ONTOLOGY = json.dumps(HARMONIZED_ONTOLOGY)

_SYSTEM_PROMPT = f"""User will input definitions in json format.
Your role is to output one or more entries in order to aggregate iteratively a harmonized ontology.

Current ontology is as follows :
BEGIN ONTOLOGY
{HARMONIZED_ONTOLOGY}
END ONTOLOGY

Your task is to reformulate this ontology entry if needed through several possibilities :
- splitting it into more atomic elements
- outputting an existant element if it expresses the same concept or a very similar one
- copying an existant element to add a possible option
- rewriting a boolean entry containing a reference to a numerical value to a number entry

You must respect the entry format and reuse the same wording as much as possible."""

EXAMPLE_1 = [
    ChatMessage(
        role="user",
        content=json.dumps(
            {
                "name": "ACCIDENT",
                "asktohuman": "Was the breakdown caused by an accident?",
                "description": "Denote if the breakdown was caused by an accident",
                "type": "boolean",
            }
        ),
    ),
    ChatMessage(
        role="assistant",
        content=json.dumps(
            {
                "name": "EVENT",
                "asktohuman": "What was the event?",
                "description": "Specify the actual event or incident",
                "type": "enum",
                "options": ["ACCIDENT"],
            }
        ),
    ),
]

EXAMPLE_2 = [
    ChatMessage(
        role="user",
        content=json.dumps(
            {
                "name": "VEHICLE_HAS_MOT_AND_ROAD_FUND_LICENCE",
                "asktohuman": "Does the vehicle have a current MOT certificate and valid road fund licence or tax disc on display?",
                "description": "Denote if the vehicle has a current MOT certificate and valid road fund licence or tax disc on display",
                "type": "boolean",
            }
        ),
    ),
    ChatMessage(
        role="assistant",
        content=json.dumps(
            [
                {
                    "name": "VEHICLE_HAS_MOT",
                    "asktohuman": "Does the vehicle have a current MOT certificate?",
                    "description": "Denote if the vehicle has a current MOT certificate",
                    "type": "boolean",
                },
                {
                    "name": "VEHICLE_HAS_ROAD_FUND_LICENCE",
                    "asktohuman": "Is there a valid road fund licence or tax disc on display?",
                    "description": "Denote if the vehicle has a valid road fund licence or tax disc on display",
                    "type": "boolean",
                },
            ]
        ),
    ),
]


def harmonize_lap(lap, harmonized_ontology, llm):
    if not harmonized_ontology:
        harmonized_ontology = HARMONIZED_ONTOLOGY

    harmonized_lap = []
    for lap_item in lap:
        harmonized_lap_item = llm.chat(
            [ChatMessage(role="system", content=_SYSTEM_PROMPT)]
            + EXAMPLE_1
            + EXAMPLE_2
            + [ChatMessage(role="user", content=json.dumps(lap_item))]
        ).message.content
        try:
            harmonized_lap_item = json.loads(harmonized_lap_item)
        except Exception as E:
            print(f"failed to load to json: {harmonized_lap_item}")
            harmonized_lap.append(lap_item)
            continue

        if isinstance(harmonized_lap_item, list):
            if len(harmonized_lap_item) > 1:
                harmonized_lap.extend(harmonized_lap_item)
                continue
            else:
                harmonized_lap_item = harmonized_lap_item[0]

        new_lap_item = {**lap_item, **harmonized_lap_item}
        harmonized_lap.append(new_lap_item)

    return harmonized_lap

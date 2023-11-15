import json
from llama_index.llms import ChatMessage

EXAMPLE_1 = {
    "name": "WAS_DRIVER_DRUNK",
    "asktohuman": "Was the driver drunk?",
    "description": "Denote if the driver has drink before driving",
    "type": "boolean",
}
EXAMPLE_1 = json.dumps(EXAMPLE_1)

LAP_EXAMPLE_1 = """// In case of destruction of your house or car following an huricane, we will pay for hotel night with a limit of 40 EUR per night. 
(EVENT="Huricane") CAUSE (EVENT="Destruction" AND (IMPACTED_OBJECT="House" OR IMPACTED_OBJECT="Car")) AND SERVICE="Hotel night" THEN LIMIT{{amount:40, unit:eur, per:night}}"""

LAP_EXAMPLE_2 = """// In case of Loss of your house, but not your car in which case it is excluded from policy, following an huricane, we will pay for hotel night with a limit of 40 EUR per night. 
(EVENT="Huricane" AND DAMAGE="Loss" AND (IMPACTED_OBJECT="House" OR (IMPACTED_OBJECT="Car") THEN EXCLUSION) AND SERVICE="Hotel night") THEN LIMIT{{amount:40, unit:eur, per:night}}"""

EMPTY_STR = "none"

_PROMPT = """You are tasked to model an insurance contract benefits into a data model. The goal of the model is to represent the bargain of the contract: What the contract covers and for how much.
If the extract of contract does not describe such a bargain do not model it and return the string "{}"

This can be done by representing Situations described in the contract using variable. 

The model can contain a boolean, date, enum or number, such as WAS_DRIVER_DRUNK.
Make the name really descriptive of what it is. In this case add the following line to describe the variable as a JSON object at the end of your answer:
{}

The output of the bargain: What will happen if the described situation is true is expressed in terms of PAYMENT, LIMIT, DEDUCTIBLE, EXCESS, EXCLUSION and COVER.

PAYMENT is used to express an amount of a payment. It uses the form PAYMENT{{amount:50, unit:usd, per:claim}}
LIMIT is used to express a limitation of a payout. It uses the form LIMIT{{amount:50, unit:usd, per:claim}}
DEDUCTIBLE is used to express a deductible. It uses the form DEDUCTIBLE{{amount:50, unit:usd, per:claim}}
EXCESS is used to express a excess. It uses the form EXCESS{{amount:50, unit:usd, per:claim}}
EXCLUSION is used to express that no benefits are offered in this situation.
COVER is used to express that a situation is covered but no specific limit or deductible applies. It uses the form COVER {{for:"<scope of cover>"}}

Do not treat the output of the bargain as ENUMS, always use the form above for EXCLUSION, LIMIT, DEDUCTIBLE and COVER.

The model itself is expressed in the form of a logic statement describing in which situation the contract applies. Use the operator AND and OR only. DO not use the operator NOT, UNLESS, CAUSE, ... . Do not list possible values in the assignation, instead create an entry per value. Use parentheses correctly. It is expressed in the following form, Prefix each logic statement by a comment (starting by //)containing the english sentence that was used to generate the statement. This sentence should not create new information, only contain the information that is already present in the text.
{}

Multiple outputs can be used in one statement, they apply to the left hand block.
{}

Each block MUST contain a list of logic statements and end with a THEN statement.

Do not try to add content that is not present in the text.

You can use the following definitions to detail any relevant concept:
{}"""


def convert_snippet_to_lap_simple(snippet, ontologies, llm):
    ontologies_str = "\n".join([json.dumps(ot) for ot in ontologies])
    lap = llm.chat(
        [
            ChatMessage(
                role="system",
                content=_PROMPT.format(
                    EMPTY_STR, EXAMPLE_1, LAP_EXAMPLE_1, LAP_EXAMPLE_2, ontologies_str
                ),
            ),
            ChatMessage(role="user", content=snippet),
        ]
    ).message.content

    if lap == EMPTY_STR:
        return None

    lap = _parse_str_to_lap(lap)
    return lap


def _parse_str_to_lap(lap_simple):
    # Parse LAP string to LAP object
    lap = []
    declarations_or_logics = lap_simple.split(
        "\n\n"
    )  # where does this double new line come from
    for declaration_or_logic in declarations_or_logics:
        if declaration_or_logic.startswith("//"):
            comment, logic = declaration_or_logic.split(
                "\n", 1
            )  # Only split on the first newline
            lap.append(logic)

        if declaration_or_logic.startswith("{"):
            declarations = declaration_or_logic.split("\n")
            for declaration in declarations:
                if declaration.startswith("{"):
                    lap.append(json.loads(declaration))
                else:
                    print(
                        f"should be declaration dict: {declaration} part of declarations {declarations} declaration_or_logic {declaration_or_logic}"
                    )

    return lap

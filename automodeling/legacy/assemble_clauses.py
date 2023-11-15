import json

PROMPT = """User will provide JSON representing a clause, you must analyze the content and output 2 lines :
- title
- classification

When relevant, title should reuse elements of the Table of Contents
---
{}
---

The classification is a string that evaluates the clause and determines to which of the following category it belongs:
- GENERAL EXCLUSION
- GENERAL CONDITION
- COVERAGE
- BENEFIT
- ENDORSEMENT

You must output a title and a classification on 2 separate lines."""

EXAMPLE_1 = {
    "type": "operator",
    "operator": "strictOr",
    "terms": [
        {
            "type": "operator",
            "operator": "and",
            "terms": [
                {
                    "type": "if",
                    "id": "eded0681-494d-4251-81e7-2430a608f80f",
                    "expressionStr": ["DRIVER_CANNOT_DRIVE", "true"],
                    "expression": {
                        "test": "equals",
                        "args": ["DRIVER_CANNOT_DRIVE", "true"],
                    },
                    "key": "Node",
                },
                {
                    "type": "if",
                    "id": "eded0681-494d-4251-81e7-2430a608f80f",
                    "expressionStr": ["NO_OTHER_ABLE_OR_QUALIFIED_DRIVER", "true"],
                    "expression": {
                        "test": "equals",
                        "args": ["NO_OTHER_ABLE_OR_QUALIFIED_DRIVER", "true"],
                    },
                    "key": "Node",
                },
                {
                    "type": "if",
                    "id": "eded0681-494d-4251-81e7-2430a608f80f",
                    "expressionStr": ["MEDICAL_CERTIFICATE_PROVIDED", "true"],
                    "expression": {
                        "test": "equals",
                        "args": ["MEDICAL_CERTIFICATE_PROVIDED", "true"],
                    },
                    "key": "Node",
                },
            ],
            "metadata": {
                "comment": '{"ops":[{"insert":"// If, during the journey, the driver cannot drive because of an injury \
                        or illness, and there is no one else able or qualified to drive the vehicle, we will recover the vehicle, \
                        driver and passengers to either finish the journey or return you to the place you were originally travelling \
                        from. You will need to provide a medical certificate for the driver before we provide assistance."}]}'
            },
        },
        {
            "type": "operator",
            "operator": "strictOr",
            "terms": [
                {
                    "type": "operator",
                    "operator": "and",
                    "terms": [
                        {
                            "type": "enum",
                            "key": "EVENT",
                            "value": "VEHICLE_BREAKDOWN",
                            "valueType": "string",
                        },
                        {
                            "type": "enum",
                            "key": "CONDITION",
                            "value": "NOT_SAFE_TO_DRIVE",
                            "valueType": "string",
                        },
                        {
                            "type": "if",
                            "id": "eded0681-494d-4251-81e7-2430a608f80f",
                            "expressionStr": ["REPAIR_TIME", "8"],
                            "expression": {
                                "test": "moreOrEquals",
                                "args": ["REPAIR_TIME", "8"],
                            },
                            "key": "Node",
                        },
                    ],
                },
                {
                    "type": "operator",
                    "operator": "and",
                    "terms": [
                        {
                            "type": "enum",
                            "key": "EVENT",
                            "value": "VEHICLE_STOLEN",
                            "valueType": "string",
                        },
                        {
                            "type": "enum",
                            "key": "CONDITION",
                            "value": "NOT_RECOVERED_WITHIN_8_HOURS",
                            "valueType": "string",
                        },
                    ],
                },
            ],
            "metadata": {
                "comment": '{"ops":[{"insert":"// If during your journey your vehicle breaks down and it is not safe \
                    to drive, and it will take at least eight hours to repair, or if it is stolen and not recovered within \
                        eight hours"}]}'
            },
        },
    ],
}


def assemble_clauses(table_of_contents, graphs):
    # classify clause
    title_and_classifications = []
    for graph in graphs:
        title_and_classification = llm(
            [
                {"role": "system", "content": PROMPT.format(table_of_contents)},
                {"role": "user", "content": json.dumps(EXAMPLE_1)},
                {
                    "role": "assistant",
                    "content": "NOT BEING ABLE TO USE YOUR VEHICLE\nCOVERAGE",
                },
                {"role": "user", "content": graph},
            ]
        )
        title_and_classifications.append(title_and_classification)

    general_conditions = {
        "title": "General Conditions",
        "rule": {
            "type": "operator",
            "operator": "and",
            "terms": [
                {"type": "rule", "key": rule["title"]}
                for rule in title_and_classification
                if title_and_classification["classification"] == "GENERAL CONDITION"
            ],
        },
    }

    coverages = {
        "title": "Coverages",
        "rule": {
            "type": "operator",
            "operator": "strictOr",
            "terms": [
                {"type": "rule", "key": rule["title"]}
                for rule in title_and_classification
                if title_and_classification["classification"] == "COVERAGE"
            ],
        },
    }

    general_exclusions = {
        "title": "General Exclusions",
        "rule": {
            "type": "operator",
            "operator": "strictOr",
            "terms": [
                {"type": "rule", "key": rule["title"]}
                for rule in title_and_classification
                if title_and_classification["classification"] == "GENERAL EXCLUSION"
            ]
            + [{"type": "bypass"}],
        },
    }

    return general_conditions, coverages, general_exclusions

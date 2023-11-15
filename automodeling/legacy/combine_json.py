import json


PROMPT = """User will provide a list of JSONs representing logic graphs.
Please combine these JSONs to make sure that only a single path matches any given situation.
You are allowed to create additional operators to group the logical elements.
Possible operators : "and", "strictOr".

Output only the JSON. Do not output non JSON content/text.
If a valid JSON cannot be generated, return { "ok": false }."""


def combine_next_json(jsons):
    combined_json = llm(
        [
            {"role": "system", "content": PROMPT},
            {
                "role": "user",
                "content": "\n---\n".join([j.decode("utf-8") for j in jsons]),
            },
        ]
    )
    if json.loads(combined_json).get("ok") is False:
        print(f"Incorrect json: {combined_json}")
        return None

    return combined_json

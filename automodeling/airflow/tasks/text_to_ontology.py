"""Module for the `text_to_ontology` task using MD representation to create an ontology.

This task leverage a previously generated MD representation of a contract to generate
a custom ontology definition as a json file.

it contains:
    * :func:`text_to_ontology`: actual logic taking an MD str and producing an ontology
        str.
    * :func:`text_to_ontology_task`: a decorated airflow task wrapping the logic to be
        used in the DAG.

"""
import json
import os
from typing import List

from automodeling.airflow.utils import airflow_task
from automodeling.tasks.text_to_ontology.main import text_to_ontology

# def text_to_ontology(md: str) -> str:
#     """Extract ontology from MD content.

#     Args:

#         md: a str representing a markdown formatted file.

#     Returns:

#         a str corresponding to a json formatted file corresponding to an ontology.
#     """
#     return "{'property': 'blue'}"


@airflow_task(s3folder_inputs=["pdf_to_text/"], s3folder_outputs=["text_to_ontology/"])
def text_to_ontology_task(text_local_path: str) -> list[tuple[str, str]]:
    """Airflow task wrapping :func:`text_to_ontology`.

    Notes:
        * s3folder_inputs lenght must match with the function args length.
        * s3folder_outputs lenght must match with the function output length.

    Args:
        md_local_path: a path to the locally downloaded MD file resolved from the
            corresponding s3folder_input and airflow io.

    Returns:

        a list of tuple containing 2 str values for each output of :func:`text_to_ontology`:
            * filename: the filename desired for the given output including extension.
            * content: the str content that will be written to the file.

    """
    # the decorator :func:`airflow_task` resolve s3 folder path into local file only
    # any further processing of the files must be defined here to accomodate
    # :func:`text_to_ontology` inputs.
    with open(text_local_path, "r") as f:
        pages: List[str] = json.loads(f.read())

    # call the pure logic function defined above.
    ontology_content = json.dumps(text_to_ontology(pages))

    # create the list of tuple for the decorator to correctly write back the file and
    # share the depedency with the next step.
    filename = os.path.basename(text_local_path).split(".")[0] + ".json"
    return [(filename, ontology_content)]

"""Task definition transforming a PDF file into a markdown file.

it exposes the following functions:
    * :func:`pdf_to_md_task`: wrapper around :func:`pdf_to_md` defined as a valide
        Airflow Task.

"""
import json
import os

from airflow.utils.context import Context

from automodeling.airflow.utils import airflow_task
from automodeling.tasks.pdf_to_md.main import pdf_to_md


@airflow_task(s3folder_inputs=["raw_pdf/"], s3folder_outputs=["pdf_to_md/"])
def pdf_to_md_task(local_pdf_path: str, context: Context) -> list[tuple[str, str]]:
    """Airflow Task converting a single PDF file into MD.

    Notes:
        * the s3folder_inputs must match the number of args
        * the s3folder_output must match the number of output

    Args:

        local_pdf_path: path to a locally downloaded pdf file from s3 resolved from the
            s3folder_inputs and airflow io.

    Returns:

        a list of tuple containing two str values:
            1. the filename desired including extension.
            2. the actual string content to write into the file.

    """
    # 1. prepare input to pdf_to_md from local file path if necessary. (in this case not
    # necessary)
    pass

    # 2. run the pdf_to_md on prepared input
    md_pages = pdf_to_md(local_pdf_path)

    if "dag_run" not in context:
        raise KeyError("`dag_run` was not found in context provided by airflow")
    run_id = context["dag_run"].run_id

    # 3. prepare output in standard format list of tuple (filename, content)
    filename = f"{run_id}/" + os.path.basename(local_pdf_path).split(".")[0] + ".json"
    return [(filename, json.dumps(md_pages))]

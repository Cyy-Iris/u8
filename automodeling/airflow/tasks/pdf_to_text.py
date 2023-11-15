"""Task definition extracting text from a PDF file.

it exposes the following functions:
    * :func:`pdf_to_text_task`: wrapper around :func:`pdf_to_text` defined as a valid
        Airflow Task.

"""
import os
import json

from automodeling.airflow.utils import airflow_task
from automodeling.tasks.pdf_to_text.main import pdf_to_text


@airflow_task(
    s3folder_inputs=["raw_pdf/"], s3folder_outputs=["pdf_to_text/"]
)
def pdf_to_text_task(local_pdf_path: str) -> list[tuple[str, str]]:
    """Airflow Task extracting text from a single PDF file.

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
    # 1. prepare input to pdf_to_text from local file path if necessary. (in this case not
    # necessary)
    pass

    # 2. run the pdf_to_text on prepared input
    content = pdf_to_text(local_pdf_path)

    # 3. prepare output in standard format list of tuple (filename, content)
    text_content = json.dumps(content)
    filename = os.path.basename(local_pdf_path).split(".")[0] + ".json"
    return [(filename, text_content)]

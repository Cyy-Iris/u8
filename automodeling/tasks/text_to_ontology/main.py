import logging
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.schema import OutputParserException

from automodeling.utils.llm import get_chain

logger = logging.getLogger(__name__)


class OntologyItem(BaseModel):
    """
    Represents an item within an ontology structure, typically used in complex systems
    like insurance, knowledge graphs, or data modeling where categorization and
    hierarchical relationships are important.

    Attributes:
        id (str): Uppercase, underscore separated, id for the ontology item.
        description (str): Description of the ontology item.
    """

    id: str = Field(
        description="Uppercase, underscore separated, id for the ontology item"
    )
    description: str = Field(description="Description of the ontology item")


class Coverage(BaseModel):
    """
    Represents an insurance coverage entity, detailing the specifics of coverage in
    an insurance policy. This class is crucial in defining the relationship between
    various risks, objects of coverage, and potential losses.

    Attributes:
        risk_item_id (str): Risk item id.
        object_of_coverage_id (str): Object of coverage id.
        loss_id (str): Loss id.
        description (str): Brief overview of the coverage.
    """

    risk_item_id: str = Field("Risk item id")
    object_of_coverage_id: str = Field("Object of coverage id")
    loss_id: str = Field("Risk item id")
    description: str = Field(description="Brief overview of the coverage")


class Ontology(BaseModel):
    """
    Represents a complete ontology structure in a specific domain, such as insurance.
    This class is a container for various lists that together form the entire ontology,
    allowing for complex relationships and structures to be defined and navigated.

    Attributes:
        risk_item_list (List[OntologyItem]): List of RISK ITEM found in the document.
        object_of_coverage_list (List[OntologyItem]): List of OBJECT OF COVERAGE found in the document.
        loss_list (List[OntologyItem]): List of LOSS found in the document.
        coverage_list (List[Coverage]): List of Coverages found in the document.
    """

    risk_item_list: List[OntologyItem] = Field(
        "List of RISK ITEM found in the document"
    )
    object_of_coverage_list: List[OntologyItem] = Field(
        "List of OBJECT OF COVERAGE found in the document"
    )
    loss_list: List[OntologyItem] = Field("List of LOSS found in the document")
    coverage_list: List[Coverage] = Field("List of Coverages found in the document")


def text_to_ontology(pages: List[str]) -> List[dict]:
    """Extract ontology from MD content.

    Args:

        pages: an array of raw text pages

    Returns:

        a str corresponding to a json formatted file corresponding to an coverage items.
    """

    ontologies: List[dict] = []
    coverages: List[dict] = []
    for pageIdx, page in enumerate(pages):
        logger.info(f"page {pageIdx + 1}/{len(pages)}...")
        result = extract_ontology_from_page(page)
        if result is not None:
            ontologies.append(result.dict())
            page_coverages = result.dict()["coverage_list"]
            for page_coverage in page_coverages:
                page_coverage["page"] = pageIdx
            coverages.extend(page_coverages)
        logger.info(f"page {pageIdx + 1}/{len(pages)} done")

    return coverages


def extract_ontology_from_page(page: str) -> Ontology | None:
    """Extract ontology from text content.
    Args:

        page: a str representing a page
        format_instructions: pydantic format instructions

    Returns:

        a dict of ontology items and a description for each
    """

    prompt_template = """
    Your are an expert at extracting ontology from insurance contracts in JSON format, \
    focusing on 'Risk Event', 'Object of Coverage', and 'Loss'. In cases of ambiguous \
    or incomplete contract text, provides your best guess, maintaining accuracy \
    while efficiently processing data.
    You will avoids giving legal advice, sticking to factual data extraction.
    ---
    Ontology item categories
    RISK EVENT: An external scenario or occurrence that activates the insurance \
        coverage. This includes events like natural disasters, accidents, thefts, and \
        other unforeseen incidents that are not related to the insured's compliance \
        with policy terms or internal conditions. \Exclude scenarios that are linked \
        to policy violations, contractual obligations, or conditions set by the insurer.
    OBJECT OF COVERAGE: The specific entity, item, or situation that the insurance \
        policy protects. This can be a physical object (like a car or home), a person \
        (in the case of health or life insurance), or a liability/circumstance (like \
        professional liability or travel disruptions).
    LOSS: The financial or material detriment that the insured suffers as a result of \
        the risk event. This refers to the actual damage, injury, cost, or liability \
        incurred by the insured, which the insurance policy is designed to compensate \
        or mitigate.
    COVERAGE: The aspect of an insurance policy that entails the combination of \
        providing protection against risk events, safeguarding the object of coverage, \
        and compensating for losses. Coverage is the assurance that, in the event of a \
        specified risk occurring, the policy will protect the insured entity or item, \
        and address the financial or material losses incurred as a result. This \
        ensures a comprehensive response to potential risks, safeguarding against \
        adverse effects and providing financial security.
    ---
    Format instructions:
    {format_instructions}
    ---
    Page to analyze:
    {page}
    ---
    Focus exclusively on extracting 'RISK_EVENT', 'OBJECT_OF_COVERAGE', 'LOSS' and \
    'COVERAGE' as defined above.
    Avoid including broader policy elements or general insurance \
    product descriptions like 'Car Insurance Policy'. Avoid including policy lifecycle \
    elements like 'Cancellation of policy' or 'Fraud'.
    Your extraction should strictly adhere to the outlined categories, disregarding \
    any other elements or general terms related to insurance products. This precision \
    is crucial to ensure that only the most relevant and specific information is \
    captured, aligning with the intended use of the data. Be vigilant in \
    differentiating between the core ontology items and broader policy descriptions or \
    categories that do not fit within the 'Risk Event', 'Object of Coverage', and \
    'Loss' definitions.
    """

    parser = PydanticOutputParser(pydantic_object=Ontology)

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["page"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = get_chain(prompt)

    response = chain.invoke({"page": page})

    try:
        return parser.parse(response["text"])
    except OutputParserException as e:
        logger.error(e)
        return None

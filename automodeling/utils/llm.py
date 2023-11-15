import os

from langchain.callbacks.base import Callbacks
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate

environment_variables = [
    "OPENAI_API_BASE",
    "OPENAI_API_VERSION",
    "AZURE_OPEN_AI_KEY",
    "OPENAI_API_TYPE",
]

for variable in environment_variables:
    if os.getenv(variable) is None:
        raise ValueError(f"{variable} is not set")

openai_api_base = os.getenv("OPENAI_API_BASE")
openai_api_version = os.getenv("OPENAI_API_VERSION")
openai_api_key = os.getenv("AZURE_OPEN_AI_KEY")
openai_api_type = os.getenv("OPENAI_API_TYPE")

# fix issues with running HTTPS call from standalone
# https://stackoverflow.com/questions/73582293/airflow-external-api-call-gives-negsignal-sigsegv-error
os.environ["no_proxy"] = "*"

llm = AzureChatOpenAI(
    openai_api_base=openai_api_base,  # type: ignore
    openai_api_version=openai_api_version,  # type: ignore
    deployment_name="PDFtoCCwithOpenAI",
    openai_api_key=openai_api_key,  # type: ignore
    openai_api_type=openai_api_type,  # type: ignore
)


def get_chain(prompt: PromptTemplate, callbacks: Callbacks = []) -> Chain:
    """
    This function initializes and returns an LLMChain with a given prompt and callbacks.

    Args:
        prompt (str): The prompt to initialize the LLMChain with.
        callbacks (Callbacks): Langchain callbacks fo

    Returns:
        Chain: An instance of LLMChain.
    """
    chain = LLMChain(llm=llm, prompt=prompt, callbacks=callbacks)
    return chain

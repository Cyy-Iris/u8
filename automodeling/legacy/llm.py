from llama_index.llms import AzureOpenAI
import os
from dotenv import load_dotenv

# Load .env variables into environment
load_dotenv()

# Retrieve environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = "https://cctoopenai.openai.azure.com"
OPENAI_API_TYPE = "azure"
OPENAI_API_VERSION = "2023-03-15-preview"


LLM = AzureOpenAI(
    deployment_name="PDFtoCCwithOpenAI",
    model_name="gpt-4",
    temperature=0,
    api_base=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY,
    api_type=OPENAI_API_TYPE,
    api_version=OPENAI_API_VERSION,
)


if __name__ == "__main__":
    from llama_index.llms import ChatMessage

    messages = [
        ChatMessage(role="system", content="your a joker"),
        ChatMessage(role="user", content="tell me a joke"),
    ]
    resp = LLM.chat(messages)
    print(resp)

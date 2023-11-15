from dotenv import load_dotenv
import os

load_dotenv()

from langchain.chat_models import AzureChatOpenAI

llm = AzureChatOpenAI(
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    deployment_name="PDFtoCCwithOpenAI",
    openai_api_key=os.getenv("AZURE_OPEN_AI_KEY"),
    openai_api_type=os.getenv("OPENAI_API_TYPE"),
)

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[])

joke = chain.invoke({"topic": "an elephant and a flying saucer"})
print(joke)

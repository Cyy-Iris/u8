import os

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langfuse.callback import CallbackHandler


load_dotenv()


llm = AzureChatOpenAI(
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    deployment_name="PDFtoCCwithOpenAI",
    openai_api_key=os.getenv("AZURE_OPEN_AI_KEY"),
    openai_api_type=os.getenv("OPENAI_API_TYPE"),
)


handler = CallbackHandler(
    public_key=os.getenv("ENV_PUBLIC_KEY"),
    secret_key=os.getenv("ENV_SECRET_KEY"),
    host=os.getenv("ENV_HOST"),
)

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])

joke = chain.invoke({"topic": "an elephant and a flying saucer"})
print(joke)

# Doesn't seem to log token usage in langfuse though the traces work fine

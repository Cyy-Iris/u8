from dotenv import load_dotenv
import os

load_dotenv()

import phoenix as px
import pandas as pd
import numpy as np

# Launch phoenix
session = px.launch_app()

# Once you have started a Phoenix server, you can start your LangChain application with the OpenInferenceTracer as a callback. To do this, you will have to instrument your LangChain application with the tracer:

from phoenix.trace.langchain import OpenInferenceTracer, LangChainInstrumentor

# If no exporter is specified, the tracer will export to the locally running Phoenix server
tracer = OpenInferenceTracer()
LangChainInstrumentor(tracer).instrument()

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
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[tracer])

joke = chain.invoke({"topic": "an elephant and a flying saucer"})

# By adding the tracer to the callbacks of LangChain, we've created a one-way data connection between your LLM application and Phoenix.

# To view the traces in Phoenix, simply open the UI in your browser.
session.url

while True:
    pass

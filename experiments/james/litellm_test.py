from dotenv import load_dotenv

load_dotenv()

import os

os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPEN_AI_KEY")
os.environ["AZURE_API_BASE"] = os.getenv("OPENAI_API_BASE")
os.environ["AZURE_API_VERSION"] = os.getenv("OPENAI_API_VERSION")

os.environ["TRACELOOP_BASE_URL"] = os.getenv("TRACELOOP_BASE_URL")

import litellm
from litellm import completion, completion_cost

litellm.set_verbose = True

# activating following line based on OpenLLMetry docs leads to an error.
# there is an example opentelemetry receiver in services to run in //
# litellm.success_callback = ["traceloop"]

# azure call
response = completion(
    model="azure/PDFtoCCwithOpenAI",
    messages=[
        {"content": "Tell me a joke about elephants and teacups.", "role": "user"}
    ],
)

print(response)

cost = completion_cost(completion_response=response)

print(f"${cost}")

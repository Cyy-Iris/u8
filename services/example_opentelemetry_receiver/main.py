from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Initialize OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Initialize FastAPI
app = FastAPI()


@app.post("/receive_trace/")
async def receive_trace(data: dict):
    with tracer.start_as_current_span("received_trace") as span:
        span.set_attribute("data_length", len(data))
        # Your logic to handle trace data, store it, etc.
    return {"message": "Trace received"}


# To run the server, use the command: uvicorn <filename>:app --reload

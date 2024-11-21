from chain import generate_ollama_stream_response
from chroma import get_patient_id
from db import get_patient_data
from extraction import extract_name
from fastapi import FastAPI
from schemas import Message
from starlette.responses import StreamingResponse
from utils import build_context

app = FastAPI()


@app.post("/generate")
async def generate_response(message: Message):
    name = extract_name(message.text)
    data = get_patient_data(get_patient_id(name))
    context = build_context(data)
    return StreamingResponse(generate_ollama_stream_response(message.text, context), media_type="text/event-stream")

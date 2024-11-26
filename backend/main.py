from chain import generate_ollama_stream_response
from chroma import get_patient_id
from db import get_patient_data
from extraction import extract_name
from fastapi import FastAPI, HTTPException
from schemas import Message
from starlette.responses import StreamingResponse
from utils import build_context

app = FastAPI()


@app.post("/generate")
async def generate_response(message: Message):
    name = extract_name(message.text)
    patient_id = get_patient_id(name)
    if not patient_id:
        raise HTTPException(status_code=404, detail="Couldn't find data for that name, please, input your name and surname clearer")
    data = get_patient_data(patient_id)
    context = build_context(data)
    return StreamingResponse(generate_ollama_stream_response(message.text, context), media_type="text/event-stream")

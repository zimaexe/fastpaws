from fastapi import FastAPI, HTTPException
from starlette.responses import StreamingResponse

from chain import generate_ollama_stream_response
from chroma import get_patient_id
from db import get_patient_data, get_patient_data_with_agent
from extraction import extract_name
from schemas import Message

app = FastAPI()


@app.post("/generate")
async def generate_response(message: Message):
    name = extract_name(message.text)
    patient_id = get_patient_id(name)
    if not patient_id:
        raise HTTPException(
            status_code=404,
            detail="Couldn't find data for that name, please, input your name and surname clearer",
        )
    context = get_patient_data_with_agent(message.text, patient_id)
    return StreamingResponse(
        generate_ollama_stream_response(message.text, context),
        media_type="text/event-stream",
    )

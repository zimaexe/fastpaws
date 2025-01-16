"""
This module provides the main entry point for generating responses
using the Ollama language model in a FastAPI application.

Endpoints:
    - /generate: POST endpoint for generating responses from the Ollama LLM.

Functions:
    generate_response(message: Message, chat_id: Annotated[str, Cookie()]):
        Generate a response from the Ollama LLM based on the user's message.

Dependencies:
    - fastapi.FastAPI
    - starlette.responses.StreamingResponse
    - chain.analyze_history
    - chain.generate_ollama_stream_response
    - chain.get_answer_from_context
    - chroma.get_patient_id
    - db.get_patient_data_with_agent
    - extraction.extract_name
    - redis_client.REDIS_CLIENT
    - schemas.Message
"""


from chain import (
    analyze_history,
    generate_ollama_stream_response,
    get_answer_from_context,
)
from chroma import get_patient_id
from db import get_patient_data_with_agent
from extraction import extract_name
from fastapi import FastAPI, HTTPException
from redis_client import REDIS_CLIENT
from schemas import Message
from starlette.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://0.0.0.0"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_response(
    message: Message
) -> StreamingResponse:
    """
    Generate a response from the Ollama LLM based on the user's message.

    Args:
        message (Message): The user's message.

    Returns:
        StreamingResponse: The response from the Ollama LLM.

    """
    print(message)

    patient_id = await REDIS_CLIENT.get_patient_id(message.chat_id)
    if not patient_id:
        name = extract_name(message.text)
        patient_id = get_patient_id(name)
        await REDIS_CLIENT.set_patient_id(message.chat_id, patient_id)

    if not patient_id:
        raise HTTPException(400, "Patient was not found")

    is_info_available = await analyze_history(message.text, message.chat_id)
    if is_info_available:
        return StreamingResponse(
            get_answer_from_context(message.text, message.chat_id),
            media_type="text/event-stream",
        )
    context = await get_patient_data_with_agent(message.text, patient_id)
    return StreamingResponse(
        generate_ollama_stream_response(message.text, context, message.chat_id),
        media_type="text/event-stream",
    )

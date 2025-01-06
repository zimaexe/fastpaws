from typing import Annotated

from chain import (analyze_history, generate_ollama_stream_response,
                   get_answer_from_context)
from chroma import get_patient_id
from db import get_patient_data_with_agent
from extraction import extract_name
from fastapi import Cookie, FastAPI
from redis_client import REDIS_CLIENT
from schemas import Message
from starlette.responses import StreamingResponse

app = FastAPI()


@app.post("/generate")
async def generate_response(message: Message, chat_id: Annotated[str, Cookie()]):
    """
    Generate a response from the Ollama LLM based on the user's message.

    Args:
        message (Message): The user's message.

    Returns:
        StreamingResponse: The response from the Ollama LLM.

    """
    print(message)

    patient_id = await REDIS_CLIENT.get_patient_id(chat_id)
    if not patient_id:
        name = extract_name(message.text)
        patient_id = get_patient_id(name)
        await REDIS_CLIENT.set_patient_id(chat_id, patient_id)

    is_info_available = await analyze_history(message.text, chat_id)
    if is_info_available:
        return StreamingResponse(
            get_answer_from_context(message.text, chat_id),
            media_type="text/event-stream",
        )
    context = await get_patient_data_with_agent(message.text, patient_id)
    return StreamingResponse(
        generate_ollama_stream_response(message.text, context, chat_id),
        media_type="text/event-stream",
    )

import json, asyncio, sqlite3
from main import generate_response
from pathlib import Path
from pydantic import BaseModel
import aiofiles

class Message(BaseModel):
    text: str

async def build_answer_string(message: Message):
    answer = ""
    res = await generate_response(message)
    async for chunk in res.body_iterator:
        answer += chunk
    return answer

async def save_message_to_file(file_path: str, message: dict):
    async with aiofiles.open(file_path, mode='w') as file:
        await file.write(json.dumps(message))


async def load_message_from_file(file_path: str) -> Message:
    async with aiofiles.open(file_path, mode='r') as file:
        data = await file.read()
    return Message(**json.loads(data))


async def call_api(prompt: str, options: dict[str, any], context: dict[str, any]) -> dict:
    # Extract configuration options from 'options' and 'context'.
    config = options.get('config', {})
    additional_option = config.get('additionalOption', None)
    user_variable = context['vars'].get('userVariable', None)
    # Save the input message to a file asynchronously.
    file_path = "storage/input.json"
    await save_message_to_file(file_path, {"text": prompt})

    # Load the message from the file asynchronously and process it.
    message = await load_message_from_file(file_path)
    output = await build_answer_string(message)

    # The result should be a dictionary with at least an 'output' field.
    result = {
        "output": output,
    }
    print(output)
    return result

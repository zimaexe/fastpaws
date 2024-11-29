# my_script.py
import json, asyncio, sqlite3
from main import generate_response
from pathlib import Path
from pydantic import BaseModel


class Message(BaseModel):
    text: str


async def build_answer_string(message: Message):
    answer = ""
    res = await generate_response(message)
    async for chunk in res.body_iterator:
        answer += chunk
    return answer
    

def call_api(prompt: str, options: dict[str, any], context: dict[str, any]):
    # Note: The prompt may be in JSON format, so you might need to parse it.
    # For example, if the prompt is a JSON string representing a conversation:
    # prompt = '[{"role": "user", "content": "Hello, world!"}]'
    # You would parse it like this:
    # prompt = json.loads(prompt)

    # The 'options' parameter contains additional configuration for the API call.
    config = options.get('config', None)
    additional_option = config.get('additionalOption', None)

    # The 'context' parameter provides info about which vars were used to create the final prompt.
    user_variable = context['vars'].get('userVariable', None)

    with open ("storage/input.json", "w") as f:
        json.dump({"text": prompt}, f)

    output = asyncio.run(build_answer_string(load_message_from_file("storage/input.json")))
    # print(output)
    # The result should be a dictionary with at least an 'output' field.
    result = {
        "output": output,
    }
    return result


def load_message_from_file(file_path: str) -> Message:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return Message(**data)


# if __name__ == "__main__":
#     print(asyncio.run(build_string(Message(text="Hi, my name is Arnold Kollar, I would like to know what medicines I took?"))))
import json
import asyncio
from pathlib import Path
from main import generate_response
from pydantic import BaseModel
import aiofiles


class Message(BaseModel):
    text: str


async def build_answer_string(message: Message) -> str:
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
    return result

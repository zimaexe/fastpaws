# my_script.py
import json, asyncio, sqlite3
from main import generate_response
from pathlib import Path
from pydantic import BaseModel
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

    output = asyncio.run(generate_response(load_message_from_file("storage/input.json")))
    # print(output)
    # The result should be a dictionary with at least an 'output' field.
    result = {
        "output": output,
    }
    return result


class Message(BaseModel):
    text: str

def load_message_from_file(file_path: str) -> Message:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return Message(**data)

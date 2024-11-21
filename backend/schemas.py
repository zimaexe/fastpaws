from pydantic import BaseModel, field_validator


class Message(BaseModel):
    text: str

    @field_validator('text')
    @classmethod
    def text_is_not_empty(cls, v: str):
        if not v:
            raise ValueError("Input cannot be empty string")
        return v

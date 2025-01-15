"""
This module defines the Pydantic models used in the backend.
Classes:
    Message: A Pydantic model representing a message from the user.
Methods:
    text_is_not_empty: A field validator method to ensure the 'text' field is not an empty string.
"""

from pydantic import BaseModel, field_validator


class Message(BaseModel):
    """
    A class to represent a message from the user.
    """

    text: str
    chat_id: str

    @field_validator("text")
    @classmethod
    def text_is_not_empty(cls, v: str) -> str | None:
        """
        Validate that the input is not an empty string.

        Args:
            v (str): The input string.

        Returns:
            str: The input string if it is not empty.
        """
        if not v:
            raise ValueError("Input cannot be empty string")
        return v

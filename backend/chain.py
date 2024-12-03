from typing import AsyncGenerator

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


async def generate_ollama_stream_response(message: str, context) -> AsyncGenerator:
    """
    Stream response from Ollama LLM based on a user question and context data.

    Args:
        message (str): User question.
        context (dict): Context data from database.

    Yields:
        str: Response from Ollama LLM.
        
    """
    template1 = """Given the following user question and context data from database, answer the user question.
    Dates are stored in year-month-day form in data. Try to answer human like and take all info from context to answer prettier.
    Take into account all provided medicines and fields and build reasonable answer. Do not include data insufficient for the use as for example analysis of bool values.
    Question: {question}
    Context: {context}
    Answer: """

    prompt = ChatPromptTemplate.from_template(template1)
    chain = prompt | OllamaLLM(model="llama3.2")
    async for chunk in chain.astream({"question": message, "context": context}):
        yield chunk

from typing import AsyncGenerator

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI

async def generate_ollama_stream_response(message: str, context):
    template1 = """Given the following user question and context data from database, answer the user question.
    Dates are stored in year-month-day form in data. Try to answer human like and take all info from context to answer prettier.
    When answering medicins or taking periods relate answers, take in mind all occurences of each medicine, so your answer will be accurate for each patients' situation
    Context gived to you is a whole known to you personal data, answer with confidence and do not specify any context or assistance. Talk directly to the user who wrote to you.
    Question: {question}
    Context: {context}
    Answer: """

    prompt = ChatPromptTemplate.from_template(template1)
    chain = prompt | ChatOpenAI(model="gpt-4o", temperature=0.1)
    async for chunk in chain.astream({"question": message, "context": context}):
        yield chunk

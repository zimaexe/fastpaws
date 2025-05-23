"""
This module provides functionality to generate responses
using the Ollama language model and analyze conversation history.

Functions:
    generate_ollama_stream_response(message: str, context: str, chat_id: str) -> AsyncGenerator:
        Asynchronously generates a response stream based on
        the given message and context using the Ollama language model.

    analyze_history(question: str, chat_id: str) -> bool:
        Analyzes the conversation history to determine if a
        question can be answered from the existing context.

    get_answer_from_context(question: str, chat_id: str) -> AsyncGenerator:
        Generates an answer from the conversation context based on the user's question.

Dependencies:
    - langchain_core.prompts.ChatPromptTemplate
    - langchain_ollama.ChatOllama
    - langchain_openai.ChatOpenAI
    - langgraph.checkpoint.memory.MemorySaver
    - redis_client.REDIS_CLIENT
"""

from typing import AsyncGenerator

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from redis_client import REDIS_CLIENT

LLM = ChatOllama(model="mistral", temperature=0.3, base_url="http://ollama:11434")
MEMORY = MemorySaver()


async def generate_ollama_stream_response(
    message: str, context: str, chat_id: str
) -> AsyncGenerator:
    """
    Stream response from Ollama LLM based on a user question and context data.

    Args:
        message (str): User question.
        context (dict): Context data from database.

    Yields:
        str: Response from Ollama LLM.
        :param name:

    """
    template1 = """
    Given the following user question and context data from database,
    answer the user question. Dates are stored in year-month-day form in data.
    Try to answer human like and take all info from context to answer prettier.
    When answering medicins or taking periods relate answers, take in mind all
    occurences of each medicine, so your answer will be accurate for each patients'
    situation. Context gived to you is a whole known to you personal data, answer
    with confidence and do not specify any context or assistance.
    Talk directly to the user who wrote to you.
    Question: {question}
    Context: {context}
    Answer: """

    prompt = ChatPromptTemplate.from_template(template1)

    chain = prompt | LLM

    answer = ""
    async for chunk in chain.astream({"question": message, "context": context}):
        answer += chunk.content
        yield chunk.content
    await REDIS_CLIENT.set_conversation_data(
        chat_id, [("user", message), ("ai", answer)]
    )


async def analyze_history(question: str, chat_id) -> bool:
    """
    Analyze conversation history to determine if a
    question can be answered from the existing context.

    Args:
        question (str): The user question.
        chat_id (str): The conversation ID.

    Returns:
        bool: True if the question can be answered from the existing context, False otherwise.
    """
    chat = (
        ChatOllama(model="mistral", temperature=0.5, base_url="http://ollama:11434")
        | StrOutputParser()
    )

    template1 = """
    Given the user question, define if it's possible to answer their question
    from existing conversation context. Answer with a word 'YES' and 'NO'
    depending on your opinion. DO NOT add any other words except this two
    and answer with only ONE word. You MUST NOT use any answer options except
    of 'YES' and 'NO', do not add any other symbols to your answer.
    When it comes to personal patient's data such as name, try to find
    it in previous messages.
    Answer: """

    inputs = {
        "messages": await REDIS_CLIENT.get_conversation_data(chat_id)
        + [
            ("system", template1.strip()),
            (
                "user",
                f"Can the next question be answered from conversation context? "
                f"Question: {question}.",
            ),
        ]
    }

    res = await chat.ainvoke(inputs["messages"])

    print(res)

    return res.strip() == "YES"


async def get_answer_from_context(question, chat_id) -> AsyncGenerator:
    """
    Generate an answer from the conversation context based on the user's question.

    Args:
        question (str): The user's question.
        chat_id (str): The conversation ID.

    Yields:
        str: The answer to the user's question.
    """

    prompt = (
        "From provided conversation context,"
        " answer the user's question with as much details as possible."
    )

    answer = ""
    chat = ChatOllama(model="mistral", temperature=0.4, base_url="http://ollama:11434")

    async for chunk in chat.astream(
        await REDIS_CLIENT.get_conversation_data(chat_id)
        + [("system", prompt), ("user", question)]
    ):
        answer += chunk.content
        yield chunk.content

    await REDIS_CLIENT.set_conversation_data(
        chat_id, [("user", question), ("ai", answer)]
    )

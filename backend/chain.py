import os
from typing import AsyncGenerator

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langgraph.checkpoint.memory import MemorySaver

from redis_client import REDIS_CLIENT

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
LLM = OllamaLLM(model="mistral", temperature=0.5, base_url="http://localhost:11434")
MEMORY = MemorySaver()

async def generate_ollama_stream_response(message: str, context: str, chat_id: str) -> AsyncGenerator:
    """
    Stream response from Ollama LLM based on a user question and context data.

    Args:
        message (str): User question.
        context (dict): Context data from database.

    Yields:
        str: Response from Ollama LLM.
        :param name:

    """
    template1 = """Given the following user question and context data from database, answer the user question.
    Dates are stored in year-month-day form in data. Try to answer human like and take all info from context to answer prettier.
    When answering medicins or taking periods relate answers, take in mind all occurences of each medicine, so your answer will be accurate for each patients' situation
    Context gived to you is a whole known to you personal data, answer with confidence and do not specify any context or assistance. Talk directly to the user who wrote to you.
    Question: {question}
    Context: {context}
    Answer: """

    prompt = ChatPromptTemplate.from_template(template1)

    chain = prompt | LLM

    # chain = prompt | OllamaLLM(model="gemma2", temperature=0.1, base_url="http://ollama:11434")
    # chain = prompt | OllamaLLM(model="mistral", temperature=0.1, base_url="http://ollama:11434")
    # chain = prompt | ChatOpenAI(model="gpt-4o", temperature=0.1) | StrOutputParser()
    answer = ""
    async for chunk in chain.astream({"question": message, "context": context}):
        answer += chunk
        yield chunk
    await REDIS_CLIENT.set_conversation_data(chat_id, [("user", message), ("ai", answer)])
    print("AFTER")
    print(answer)


async def analyze_history(question: str, chat_id):
    # LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0) # tests with another LLM
    template1 = f"""Given the following user question and conversation history, define if user question can be answered from the existing chat messages.
    As answer options use only words 'YES' or 'NO' depending on your final opinion. Analyze if user already provided relevant info in their questions, or if answer can be found in assistant's answers.
    Examples: User provided their name in previous messages, medications info is already known.
    Question: {question}
Answer: """
    inputs = {
        "messages": await REDIS_CLIENT.get_conversation_data(chat_id) + [("system", template1), ("user", question)]
    }
    res = await LLM.ainvoke(inputs["messages"])
    print()

    return res.strip() == "YES"


async def get_answer_from_context(question, chat_id):
    prompt = "From provided chat history, answer the user's question with as much details as possible"
    answer = ""
    async for chunk in LLM.astream(
            await REDIS_CLIENT.get_conversation_data(chat_id) + [("system", prompt), ("user", question)]
    ):
        answer += chunk
        yield chunk
    await REDIS_CLIENT.set_conversation_data(chat_id, [("user", question), ("ai", answer)])

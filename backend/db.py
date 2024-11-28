import sqlite3
from datetime import date
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from langchain import hub
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

DB_PATH = Path(__file__).parent / "storage" / "patients.db"
PROMPT_TEMPLATE = hub.pull("langchain-ai/sql-agent-system-prompt")


async def upload_patients_data(csv_path: Path) -> None:
    with sqlite3.connect(DB_PATH) as db:
        pd.read_csv(csv_path).to_sql("patients", db, if_exists="replace")


def get_patient_data(patient_id: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.execute(
            "SELECT * FROM patients WHERE patient_id = ?", (patient_id,)
        )
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return pd.DataFrame(rows, columns=columns)


def build_prompt(patient_id: str) -> str:
    sql_prompt = PROMPT_TEMPLATE.format(dialect="SQLite", top_k=10)
    return f"""Context info: 
    Today is {date.today()}
    Id of the patient is {patient_id}
    Context Instructions: Column names are in Slovak language. Each medication for specified amount of days costs only specified amount of money, do not do the product.
    When patient asks about medication without specifying period, take into account all taking periods, so all occurences of specified medicine for this specific patient.
    Answer Instructions: Collect from database as much data on dates and periods of medications taking as possible. Return the context not like an natural answer, bu like a stringified tabular data. Return type is string.
    SQL Instructions: {sql_prompt}
    """


def get_sql_agent(patient_id: str):
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    return create_react_agent(
        llm, toolkit.get_tools(), state_modifier=build_prompt(patient_id)
    )


def get_patient_data_with_agent(question: str, patient_id: str):
    agent = get_sql_agent(patient_id)
    return agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        {"recursion_limit": 100},
        stream_mode="values",
    )["messages"][-1].content

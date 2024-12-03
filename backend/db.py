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
    """
    Upload patient data from a CSV file to the SQLite database.
    
    Args:
        csv_path (Path): Path to the CSV file with patient data.
    """
    with sqlite3.connect(DB_PATH) as db:
        pd.read_csv(csv_path).to_sql("patients", db, if_exists="replace")


def get_patient_data(patient_id: str) -> pd.DataFrame:
    """
    Retrieve patient data from the SQLite database by patient ID.
    
    Args:
        patient_id (str): The patient ID.

    Returns:
        pd.DataFrame: Patient data.

    """

    with sqlite3.connect(DB_PATH) as db:
        cursor = db.execute(
            "SELECT * FROM patients WHERE patient_id = ?", (patient_id,)
        )
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return pd.DataFrame(rows, columns=columns)


def build_prompt(patient_id: str) -> str:
    """
    Build a contextual prompt for a SQL-based agent using patient ID.

    Args:
        patient_id (str): The patient ID.

    Returns:
        str: A formatted prompt containing context and SQL instructions.

    """
    sql_prompt = PROMPT_TEMPLATE.format(dialect="SQLite", top_k=10)
    return f"""Context info: 
    Today is {date.today()}
    Id of the patient is {patient_id}
    SQL Instructions: {sql_prompt}
    """


def get_sql_agent(patient_id: str):
    """
    Create a SQL-based agent with a given patient ID.
    
    Args:
        patient_id (str): The patient ID.
        
    Returns: A SQL-based agent.
    """
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    return create_react_agent(
        llm, toolkit.get_tools(), state_modifier=build_prompt(patient_id)
    )


def get_patient_data_with_agent(question: str, patient_id: str) -> str:
    """
        Retrieves patient data using a SQL-based agent to answer a specific question.

        Args:
            question (str): The user question.
            patient_id (str): The patient ID.

        Returns:
            str: The answer to the user question.
    """
    agent = get_sql_agent(patient_id)
    answer = ""
    return agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        {"recursion_limit": 40},
        stream_mode="values",
    )["messages"][-1].content

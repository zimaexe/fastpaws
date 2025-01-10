import pathlib

import chromadb
import pandas as pd

client = chromadb.PersistentClient(path=str(pathlib.Path(__file__).parent.joinpath("storage/chroma")))
collection = client.get_or_create_collection("patients")


def add_patients(patients: pd.DataFrame):
    """
    Add unique patients to the collection.

    Args:
        patients (pd.DataFrame): DataFrame with patient data.
            Must include columns 'patient_id', 'meno', and 'priezvisko'.

    Raises:
        AssertionError: If the 'patient_id' column contains duplicate values.

    """
    df = patients.drop_duplicates("patient_id")
    assert len(df["patient_id"]) == len(set(patients["patient_id"]))
    collection.add(
        documents=df[["meno", "priezvisko"]].agg(" ".join, axis=1).to_list(),
        ids=df["patient_id"].to_list(),
    )


def get_patient_id(name: str) -> str:
    """
    Retrieve patient ID based on the patient name from the ChromaDB collection.

    Args:
        name (str): The full name of the patient (e.g., "John Doe").

    Returns:
        str: The patient ID if a close match is found, otherwise an empty string.
        
    """

    result = collection.query(query_texts=[name], n_results=1)
    if abs(result["distances"][0][0]) > 0.3:
        return ""
    return result["ids"][0][0]

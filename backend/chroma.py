import chromadb
import pandas as pd

client = chromadb.PersistentClient(path="./storage/chroma")
collection = client.get_or_create_collection("patients")


def add_patients(patients: pd.DataFrame):
    df = patients.drop_duplicates("patient_id")
    assert (len(df["patient_id"]) == len(set(patients["patient_id"])))
    collection.add(
        documents=df[["meno", "priezvisko"]].agg(" ".join, axis=1).to_list(), ids=df["patient_id"].to_list()
    )


def get_patient_id(name: str) -> str:
    result = collection.query(query_texts=[name], n_results=1)
    if abs(result["distances"][0][0]) > 0.3:
        return ""
    return result["ids"][0][0]

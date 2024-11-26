import sqlite3
from pathlib import Path

import pandas as pd


async def upload_patients_data(csv_path: Path) -> None:
    with sqlite3.connect(Path(__file__).parent / "storage" / "patients.db") as db:
        pd.read_csv(csv_path).to_sql("patients", db, if_exists="replace")


def get_patient_data(patient_id: str) -> pd.DataFrame:
    with sqlite3.connect(Path(__file__).parent / "storage" / "patients.db") as db:
        cursor = db.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return pd.DataFrame(rows, columns=columns)

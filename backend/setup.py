import asyncio
from pathlib import Path

import pandas as pd

from chroma import add_patients
from db import upload_patients_data


async def setup():
    """
    Upload patient data to the SQLite database and add patients to the ChromaDB collection.
    """
    csv_path = Path(__file__).parent / "storage" / "data" / "dataset.csv"
    await upload_patients_data(csv_path)
    data = pd.read_csv(csv_path)
    add_patients(data)


if __name__ == "__main__":
    asyncio.run(setup())

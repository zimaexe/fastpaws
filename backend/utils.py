import pandas as pd


def build_context(patient_data: pd.DataFrame) -> str:
    """
    Build a context string from patient data.

    Args:
        patient_data (pd.DataFrame): DataFrame with patient data.

    Returns:
        str: A formatted string containing patient data.
    """
    template = "Medicine: {}, Taking start: {}, Taking End: {}, Taking days: {}, Price: {}, Amount {}, is medicine taken away {}, insurance company paid {}\n"
    context = ""
    for row in patient_data.iterrows():
        row = row[1]
        context += template.format(
            row["nazov_lieku"],
            row["datum_predpisu"],
            row["datum_konca"],
            row["obdobie_lieku_dni"],
            row["cena"],
            row["mnozstvo"],
            row["liek_vybral"] == 1,
            row["poistovna_zaplatila_spravne"] == 1,
        )

    return context

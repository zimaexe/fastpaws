import pandas as pd


def build_context(patient_data: pd.DataFrame) -> str:
    template = "Medicine: {}, Taking start: {}, Taking End: {}, Price: {} is medicine taken away {}, insurance company paid {}\n"
    context = ""
    for row in patient_data.iterrows():
        row = row[1]
        context += template.format(
            row["nazov_lieku"],
            row['datum_predpisu'],
            row['datum_konca'],
            row['cena'],
            row['liek_vybral'] == 1,
            row['poistovna_zaplatila_spravne'] == 1
        )

    return context

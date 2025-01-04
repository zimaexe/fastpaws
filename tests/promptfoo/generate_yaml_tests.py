import pandas as pd
import sys

#Prompt 1
#Q: My name is {patient_name}. What are the names of the drugs prescribed to me?
#A: {List of drug names}
def prompt1(df, first_name, last_name):
    filtred = df[(df['meno'].str.lower() == first_name.lower()) &
            (df['priezvisko'].str.lower() == last_name.lower())]
    return str(set((filtred['nazov_lieku'].values)))

#Prompt 2
#Q: My name is {patient_name}. How many days was my {medication_name} supposed to last?
#A: {Duration in days}//return list of every time the drug was prescribed to the patient
def prompt2(df, first_name, last_name, drug_name):
    filtred = df[(df['meno'].str.lower() == first_name.lower()) &
            (df['priezvisko'].str.lower() == last_name.lower())&
                (df['nazov_lieku'].str.lower() == drug_name.lower())]
    if filtred.empty:
        return f"No record found for {first_name} {last_name} with medication {drug_name}."
    return str(set(filtred[filtred['nazov_lieku'].str.lower() == drug_name.lower()]['obdobie_lieku_dni'].values))

#Prompt 3
#Q: My name is {patient_name}. Did the insurance company pay for all my medications?
#A: {Yes/No, followed by details of which medications were/weren't paid}
def prompt3(df, first_name, last_name):
    filtred = df[(df['meno'].str.lower() == first_name.lower()) &
            (df['priezvisko'].str.lower() == last_name.lower())]
    if (filtred['poistovna_zaplatila_spravne'] == "Áno").all():
        return "Yes"
    else:
        not_paid = set(filtred[filtred['poistovna_zaplatila_spravne'] == "Nie"]['nazov_lieku'].values)
        return f"No, you need to pay: {str(not_paid)}"

#Prompt 4
#Q: My name is {patient_name}. What price did I pay for {medication_name}?
#A: {Price paid}
def prompt4(df, first_name, last_name, drug_name):
    filtred = df[(df['meno'].str.lower() == first_name.lower()) &
            (df['priezvisko'].str.lower() == last_name.lower())&
                (df['nazov_lieku'].str.lower() == drug_name.lower())
            ]
    if filtred.empty:
        return f"No record found for {first_name} {last_name} with medication {drug_name}."
    res = str(set(filtred[filtred['nazov_lieku'].str.lower() == drug_name.lower()]['cena'].values))
    return f"You paid {res}"

#Prompt 5
#Q: My name is {patient_name}. On which date was my prescription for {medication_name} issued?
#A: {Date of prescription issuance}
def prompt5(df, first_name, last_name, drug_name):
    filtred = df[(df['meno'].str.lower() == first_name.lower()) &
            (df['priezvisko'].str.lower() == last_name.lower())&
                (df['nazov_lieku'].str.lower() == drug_name.lower())]
    if filtred.empty:
        return f"No record found for {first_name} {last_name} with medication {drug_name}."
    res = str(set(filtred[filtred['nazov_lieku'].str.lower() == drug_name.lower()]['datum_predpisu'].values))
    return f"You were prescribed {drug_name} on {res}"

# Prompt 6
# Q: My name is {patient_name}. Did I collect my {medication_name}
# A: {Yes/No}
def prompt6(df, first_name, last_name, drug_name):
    filtered = df[(df['meno'].str.lower() == first_name.lower()) &
                (df['priezvisko'].str.lower() == last_name.lower()) &
                (df['nazov_lieku'].str.lower() == drug_name.lower())]
    if filtered.empty:
        return f"No record found for {first_name} {last_name} with medication {drug_name}."
    if (filtered['liek_vybral'] == "Áno").all():
        return f"Yes, you collected {drug_name}"
    else:
        return "No you did not collect all your medications, you need to took: " + str(set(filtered[filtered['liek_vybral'] == "Nie"]['nazov_lieku'].unique()))

#Prompt 7
#Q: My name is {patient_name}. What is the quantity of {medication_name} prescribed to me?
#A: {Quantity}
def prompt7(df, first_name, last_name, drug_name):
    filtered = df[(df['meno'].str.lower() == first_name.lower()) &
                (df['priezvisko'].str.lower() == last_name.lower()) &
                (df['nazov_lieku'].str.lower() == drug_name.lower())]
    if filtered.empty:
        return f"No record found for {first_name} {last_name} with medication {drug_name}."
    return f"The quantity of {drug_name} prescribed to you is {str(set(filtered['mnozstvo'].values))}"

#Prompt 8
#Q: My name is {patient_name}. What is the end date for my prescription period for {medication_name}?
#A: {End date}
def prompt8(df, first_name, last_name, drug_name):
    filtered = df[(df['meno'].str.lower() == first_name.lower()) &
                (df['priezvisko'].str.lower() == last_name.lower()) &
                (df['nazov_lieku'].str.lower() == drug_name.lower())]
    if filtered.empty:
        return f"No record found for {first_name} {last_name} with medication {drug_name}."

    return f"The end date for your prescription period for {drug_name} is {filtered['datum_konca'].values}"

#Prompt 9
#Q: My name is {patient_name}. How much money did I pay for all my medications?
#A: {Total cost for all medications}
def prompt9(df, first_name, last_name):
    filtered = df[(df['meno'].str.lower() == first_name.lower()) &
                (df['priezvisko'].str.lower() == last_name.lower())]
    if filtered.empty:
        return f"No record found for {first_name} {last_name}."
    return f"You paid {str(round(filtered['cena'].sum(), 2))} for all your medications"

# Prompt 10
# Q: My name is {patient_name}. What is my gender?
# A: {Gender, e.g., Male/Female}
def prompt10(df, first_name, last_name):
    filtered = df[(df['meno'].str.lower() == first_name.lower()) &
                (df['priezvisko'].str.lower() == last_name.lower())]
    if filtered.empty:
        return f"No record found for {first_name} {last_name}."
    if filtered.iloc[0]['pohlavie'] == 'M':
        return "You are man"
    else:
        return "You are woman"

def generate_10_prompts(df, name, surname, drug_name):
    print(f"""  - vars:
      promt: My name is {name} {surname}. What are the names of the drugs prescribed to me?""")

    print(f"""    assert:
      - type: model-graded-closedqa
        value: \"{prompt1(df, name, surname)}\"""")

    print(f"""  - vars:
      promt: My name is {name} {surname}. How many days was my {drug_name} supposed to last?""")
    print(f"""    assert:
      - type: model-graded-closedqa
        value: \"{str(prompt2(df, name, surname, drug_name)).replace("\n", ' ')}\"""")

    print(f"""  - vars:
      promt: My name is {name} {surname}. Did the insurance company pay for all my medications?""")
    print(f"""    assert:
      - type: model-graded-closedqa
        value: \"{prompt3(df, name, surname)}\"""")

    print(f"""  - vars:
      promt: My name is {name} {surname}. What price did I pay for {drug_name}?""")
    print(f"""    assert:
      - type: model-graded-closedqa
        value: \"{prompt4(df, name, surname, drug_name)}\"""")

    print(f"""  - vars:
      promt: My name is {name} {surname}. On which date was my prescription for {drug_name} issued?""")
    print(f"""    assert:
      - type: model-graded-closedqa
        value: \"{prompt5(df, name, surname, drug_name)}\"""")

    print(f"""  - vars:
      promt: My name is {name} {surname}. Did I collect my {drug_name}?""")
    print(f"""    assert:
      - type: model-graded-closedqa
        value: \"{prompt6(df, name, surname, drug_name)}\"""")

    print(f"""  - vars:
      promt: My name is {name} {surname}. What is the quantity of {drug_name} prescribed to me?""")
    print(f"""    assert:
      - type: model-graded-closedqa
        value: \"{prompt7(df, name, surname, drug_name)}\"""")

    print(f"""  - vars:
      promt: My name is {name} {surname}. What is the end date for my prescription period for {drug_name}?""")
    print(f"""    assert:
      - type: model-graded-closedqa
        value: \"{prompt8(df, name, surname, drug_name)}\"""")

    print(f"""  - vars:
      promt: My name is {name} {surname}. How much money did I pay for all my medications?""")
    print(f"""    assert:
      - type: model-graded-closedqa
        value: \"{prompt9(df, name, surname)}\"""")

    print(f"""  - vars:
      promt: My name is {name} {surname}. What is my gaender?""")
    print(f"""    assert:
      - type: model-graded-closedqa
        value: \"{prompt10(df, name, surname)}\"""")

if __name__ == "__main__":
    file_path = 'storage/data/dataset.csv'
    dataset = pd.read_csv(file_path)
    number_of_patiens = len(set(dataset["patient_id"]))

    with open('promptfooconfig.yaml', 'w', encoding='utf-8') as file:
        sys.stdout = file
        print("""description: "QA Bot evaluation"

prompts:
  - "{{promt}}"
providers:
  - id: http
    config:
      url: http://backend:8000/generate
      method: POST
      headers:
        Content-Type: application/json
      body:
        text: "{promt}"
tests: """)

        for i in range(10):
            name = dataset.iloc[i]['meno']
            surname = dataset.iloc[i]['priezvisko']
            drug_name = dataset.iloc[i]['nazov_lieku']
            generate_10_prompts(dataset, name, surname, drug_name)

from transformers import pipeline

model_name = "deepset/roberta-base-squad2"

qa_pipeline = pipeline("question-answering", model=model_name, tokenizer=model_name)


def extract_name(message: str) -> str:
    return qa_pipeline(question="What is the user's name?", context=message)["answer"]

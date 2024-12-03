from transformers import pipeline

model_name = "deepset/roberta-base-squad2"

qa_pipeline = pipeline("question-answering", model=model_name, tokenizer=model_name)


def extract_name(message: str) -> str:
    """
    Extract the user's name from the message using a question-answering model.

    Args:
        message (str): The user's message.

    Returns:
        str: The extracted name.
    """
    return qa_pipeline(question="What is the user's name?", context=message)["answer"]

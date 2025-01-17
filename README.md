# FastPaws

FastPaws is a Q&A system which uses Large Language Models (LLM) technology  and this system designed to help users obtain information from insurance companies. It facilitates communication with company databases, making it easier for people to get the answers they need.

This project was a semestral project made as part of the Artificial Intelligence course at the uni.

## Members

@matoH12 (mentor)

@faurdent (backend)

@zimaexe (backend/testing)

@waterscape03 (backend/documentation)

@vadim-ghostman (project manager)

@krrysanova (webmaster)

@Kostianets (design/presentation)

## Stack

Redis, Langchain, ChromaDB, ollama, FastAPI, SQLite, Pandas, [RoBERTa](https://huggingface.co/docs/transformers/model_doc/roberta)

## Service

Project is divided on backend and frontend part

### Backend

To run the backend locally do the following steps:

1. Upload `dataset.csv` file to the `backend/storage/data` directory if it's not there.
2. Setup `llama3.2` model locally with `ollama`.
3. Install poetry environment
4. From project **root directory** run `poetry shell` and `poetry install --no-root` commands.
5. Go to the `backend` directory
6. Run `python setup.py` to setup SQL and vector stores
7. Start server by `fastapi dev main.py`
8. Endpoints will be availiable at `http://127.0.0.1:8000/docs`.

### Frontend

To run the frontend locally do the following steps:

1. Go to `frontend` directory
2. Run `npm install` to install dependencies
3. Run `npm run local` to run server at `http://localhost:5173`

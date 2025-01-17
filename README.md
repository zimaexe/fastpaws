# FastPaws

FastPaws is a Q&A system which uses Large Language Models (LLM) technology  and this system designed to help users obtain information from insurance companies. It facilitates communication with company databases, making it easier for people to get the answers they need.

This project was a semestral project made as part of the Artificial Intelligence course at the uni.

## Members

[@matoH12](https://github.com/matoH12) (mentor)

[@faurdent](https://github.com/faurdent) (backend)

[@zimaexe](https://github.com/zimaexe) (backend/testing)

[@waterscape03](https://github.com/waterscape03) (backend/documentation)

[@vadim-ghostman](https://github.com/vadim-ghostman) (project manager)

[@krrysanova](https://github.com/krrysanova) (webmaster)

[@Kostianets](https://github.com/Kostianets) (design/presentation)

## Stack

Redis, Langchain, ChromaDB, ollama, FastAPI, SQLite, Pandas, [RoBERTa](https://huggingface.co/docs/transformers/model_doc/roberta)

## Setting up environment using Docker

> [!NOTE]
> Install `docker-compose` and `docker` in your system
> and create `.env` file in **root directory** from `.env.example` template

> [!TIP]
> You can use ready Docker image by specifying `zemberovka` in
> `DOCKER_USERNAME` environment variable, but if you want, build environment by `docker compose build`

To start backend and frontend servers, run `docker compose up -d`

### Availiability

- Backend endpoints will be availiable from `http://localhost:8000/docs`

- Web application will be availiable from `http://localhost`

## Setting up environment without Docker

### Backend

> [!NOTE]
> Create `.env` file in **root directory** from `.env.example` template

To run the backend locally do the following steps

1. Upload `dataset.csv` file to the `backend/storage/data` directory if it's not there
2. Setup `llama3.2` model locally with `ollama`
3. Install poetry environment
4. From project **root directory** run `poetry shell` and `poetry install --no-root` commands.
5. Go to the `backend` directory
6. Run `python setup.py` to setup SQL and vector stores
7. Start server by `fastapi dev main.py`
8. Endpoints will be availiable at `http://localhost:8000/docs`

### Frontend

> [!NOTE]
> Create `.env` file in **root directory** from `.env.example` template and
> provide `BACKEND_ADDRESS`

To run the frontend locally do the following steps:

1. Go to `frontend` directory
2. Run `npm install` to install dependencies
3. Run `npm run dev` to run server at `http://localhost`

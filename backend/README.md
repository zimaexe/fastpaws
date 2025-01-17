# Backend

> [!NOTE]
> Create `.env` file in **root directory** from `.env.example` template

To run the backend locally do the following steps:

1. Upload `dataset.csv` file to the `storage/data` directory if it's not there.
2. Install and setup `llama3.2` and `mistral` model locally with `ollama`
3. Install poetry environment
4. From project **root directory** run `poetry shell` and `poetry install --no-root` commands.
5. Return to the `backend` directory
6. Run `python setup.py` to setup SQL and vector stores
7. Start server by `fastapi dev main.py`
8. Endpoints will be availiable at `http://localhost:8000/docs`.
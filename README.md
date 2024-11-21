# UI-projekt-QA-bot

## Backend

To run the backend locally do the following steps:
1. Upload dataset.csv file to the `./backend/storage/data` folder if it's not there.
2. Setup `llama3.2` model locally with ollama.
3. Install poetry environment
4. From project root folder run `poetry shell` and `poetry install --no-root` commands.
5. Go to the backend directory `cd ./backend`
6. Run `python setup.py` to setup SQL and vector stores
7. Run `fastapi dev main.py`
8. Go to the `http://127.0.0.1:8000/docs` to test endpoint.

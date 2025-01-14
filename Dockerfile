FROM python:3.12

WORKDIR /app

RUN pip install -U pip && pip install poetry

RUN poetry config virtualenvs.create false

COPY . /app/

RUN poetry check

RUN poetry install --no-root

EXPOSE 8000

WORKDIR /app/backend

RUN python3.12 setup.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

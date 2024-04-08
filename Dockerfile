FROM python:3.11-slim

RUN pip install poetry==1.8.2

WORKDIR /app

COPY . .

RUN poetry install

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

FROM python:3.8

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install --upgrade pip && \
    pip install poetry

RUN poetry install --no-dev

WORKDIR /app

COPY app .

EXPOSE 8888

CMD ["poetry", "run", "python", "index.py"]

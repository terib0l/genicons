# Build stage
FROM python:3.8

COPY pyproject.toml .

RUN pip install --upgrade pip && \
    pip install poetry

RUN poetry install --no-dev

WORKDIR /app

COPY app .

EXPOSE 8888

COPY .env /

CMD ["python", "index.py"]

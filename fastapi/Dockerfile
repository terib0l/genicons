FROM python:3.8

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip && \
    pip install poetry
COPY ./pyproject.toml /usr/src/app
RUN poetry install --no-dev

COPY . /usr/src/app

EXPOSE 8888

CMD ["poetry", "run", "python", "index.py"]

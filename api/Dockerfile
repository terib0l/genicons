# Build stage
FROM python:3.8

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

WORKDIR /app

COPY app .

EXPOSE 8888

COPY .env /

CMD ["python", "index.py"]

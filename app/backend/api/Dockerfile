FROM python:3.8

WORKDIR /usr/src/api
#COPY 
RUN pip install -r requirements.txt

# コンテナ起動後、FastAPIアプリの起動
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]

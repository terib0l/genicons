# Build stage
FROM python:3.8 AS build

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

# Run stage
FROM python:3.8 as run

RUN groupadd -r genicons && \
    useradd -r -g genicons -s /sbin/nologin genicons

WORKDIR /app

RUN chown -R genicons /app

COPY --from=build /root/.local /home/genicons/.local

RUN chown -R genicons /home/genicons

RUN mkdir -p /var/log/gunicorn && \
    chown -R genicons /var/log/gunicorn

USER genicons

COPY app .

EXPOSE 8888

CMD ["/home/genicons/.local/bin/gunicorn"]

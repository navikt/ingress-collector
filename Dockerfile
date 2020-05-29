FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8
RUN apk update && apk add ca-certificates && rm -rf /var/cache/apk/*
RUN pip install --upgrade pip

COPY requirements.txt /app/.
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py /app/
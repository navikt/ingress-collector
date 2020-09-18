FROM navikt/python:3.8
#python:3.8-slim

RUN apt-get update && apt-get install -y netcat curl

COPY . /app
WORKDIR /app
RUN mkdir tmp
RUN ls

RUN pip3 install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

ENTRYPOINT []
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]


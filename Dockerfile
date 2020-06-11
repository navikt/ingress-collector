FROM navikt/common:0.1 AS navikt-common
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8
COPY --from=navikt-common /init-scripts /init-scripts
RUN pip install --upgrade pip
RUN mkdir -p tmp
COPY *.txt /app/
COPY prestart.sh /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./collector /app/collector
COPY *.py /app/
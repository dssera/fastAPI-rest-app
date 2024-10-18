FROM python:3.9.13-slim-buster
LABEL authors="Dessera"

WORKDIR /usr/local/app

RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
EXPOSE 5000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]

FROM python:3.9.13-slim-buster

LABEL authors="Dessera"

WORKDIR /usr/local/app

# there is no && in exec mode, so I used shell one
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
EXPOSE 5000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]
# docker build -t notes-app-img .
# docker run -d --name notes-app-c --network notes-net -e POSTGRES_PASSWORD=12345 -p 8080:5000 notes-app-img
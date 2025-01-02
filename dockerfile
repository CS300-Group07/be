FROM python:3.9-slim

WORKDIR /app 

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

RUN pip install -r requirements.txt


COPY . .

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]

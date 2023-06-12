FROM python:3.10-slim-buster

# Path: /app
WORKDIR /app

# Path: /app/requirements.txt
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Path: /app
COPY unml ./unml

CMD ["python", "unml/main.py"]

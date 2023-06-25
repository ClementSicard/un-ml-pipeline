FROM --platform=arm64 python:3.10

WORKDIR /app

# Path: /app/requirements.txt
COPY requirements.txt requirements.txt

# # Install git
# RUN apk update
# RUN apk add git gcc

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Install spaCy ner model
RUN python -m spacy download en_core_web_sm

# Path: /app
COPY unml ./unml

# Purge pip cache
RUN pip cache purge


# Start FastAPI server
CMD ["uvicorn", "unml.api:app", "--host", "0.0.0.0", "--port", "80"]

# Set the base image to Python 3.10
FROM --platform=arm64 python:3.10 as builder

# Set the working directory
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Create a virtual environment and install dependencies in it.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Download spaCy ner model
RUN python -m spacy download en_core_web_trf

# Now, we will use a fresh image but copy the virtual environment we built.
# This will give us a smaller final image.
FROM --platform=arm64 python:3.10

WORKDIR /app

# Copy venv with all the installed dependencies
COPY --from=builder /opt/venv /opt/venv

# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application files
COPY unml ./unml

# Start FastAPI server
CMD ["uvicorn", "unml.api:app", "--host", "0.0.0.0", "--port", "80"]

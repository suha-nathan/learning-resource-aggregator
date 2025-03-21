# Python base image (lightweight)
FROM python:3.12-slim

# Working directory inside container
WORKDIR /usr/src/app

# Install dependencies first to use Docker cache efficiently
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the aggregation scripts and scheduler
COPY . .

# Run scheduler script
CMD ["python", "scheduler.py"]

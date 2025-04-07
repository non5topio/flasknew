# FROM python:3.10-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY . .

# CMD ["python", "app.py"]



# Base stage
FROM python:3.10-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Test stage
FROM base AS test

# Run test command
CMD ["pytest"]  

FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy project files
COPY backend/pyproject.toml backend/poetry.lock* ./

# Configure poetry to not create a virtual environment in the container directly
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

# Copy all application code
COPY backend ./

ENV PYTHONPATH=/app/backend

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.9-slim


# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /code

# lets us import from folders inside /code directly
ENV PYTHONPATH=/code

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY our code folder to docker
COPY ../.. /code/

# keep our docker container running
CMD ["tail", "-f", "/dev/null"]

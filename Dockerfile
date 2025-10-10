# 3. Dockerfile
# Build file for the 'web' service

FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /usr/src/app

# Install system dependencies needed by mysqlclient
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev gcc **pkg-config** \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install packages
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project code
COPY . /usr/src/app/

# Default command to run the Django server
CMD ["gunicorn", "task_manager_api.wsgi:application", "--bind", "0.0.0.0:8000", "--proxy-allow-from", "*"]
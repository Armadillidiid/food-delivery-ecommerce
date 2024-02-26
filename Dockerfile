# Use a smaller base image
FROM python:3.9-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the current directory contents
COPY . /app

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Combine RUN commands and remove temporary files
# RUN apt-get update \
#     && apt-get -y install build-essential libpq-dev gcc \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# Copy only necessary files
COPY ./requirements.txt /requirements.txt

# Install dependencies
RUN --mount=type=cache,target=/root/.cache \
    pip install --no-cache-dir -r /requirements.txt

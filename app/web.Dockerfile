FROM python:3.11-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Bun
RUN curl -fsSL https://bun.sh/install | bash

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --progress-bar off --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Initialize and export the reflex app
RUN reflex export --frontend-only --no-zip

FROM nginx

COPY --from=builder /app/.web/_static /usr/share/nginx/html
COPY ./nginx.conf.template /etc/nginx/templates/nginx.conf.template
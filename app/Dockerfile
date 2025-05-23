FROM python:3.11-slim

ENV REDIS_URL=redis://redis PYTHONUNBUFFERED=1 

WORKDIR /app
COPY . .

# Install setuptools and wheel first
RUN pip install --upgrade pip setuptools wheel

# Then install requirements
RUN pip install -r requirements.txt

ENTRYPOINT ["reflex", "run", "--env", "prod", "--backend-only", "--loglevel", "debug"]
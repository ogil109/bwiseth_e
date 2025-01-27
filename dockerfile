### Stage 1: Build .env file from config.json
FROM python:3.12.6-slim AS app-env
WORKDIR /app
# Generate the .env file from the JSON file, flattening nested objects
COPY config.json .
RUN mkdir /shared_env
RUN apt-get update && apt-get install -y jq && \
    jq -r '.. | select(type == "object") | to_entries[] | select(.value | type == "object") | .key as $parent | .value | to_entries[] | ($parent + "_" + .key) + "=" + (.value | tostring)' config.json > /shared_env/.env

### Stage 2: Build the application
FROM app-env AS app
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry install
COPY . .
EXPOSE 8000
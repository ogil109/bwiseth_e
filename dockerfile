# Use the official Python image as a base
FROM python:3.12.6-slim

# Set the working directory to /app
WORKDIR /app

# Generate the .env file from the JSON file, flattening nested objects
COPY config.json .
RUN jq -r '.. | select(type == "object") | to_entries[] | select(.value | type == "object") | .key as $parent | .value | to_entries[] | ($parent + "_" + .key) + "=" + (.value | tostring)' config.json > .env

# Copy the pyproject.toml and poetry.lock files into the container
COPY pyproject.toml poetry.lock ./

# Install the dependencies using Poetry
RUN poetry install

# Copy the rest of the code into the container
COPY . .

# Expose the port that your app uses (if any)
EXPOSE 8000
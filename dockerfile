# Use the official Python image as a base
FROM python:3.12.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files into the container
COPY pyproject.toml poetry.lock ./

# Install the dependencies using Poetry
RUN poetry install

# Copy the rest of the code into the container
COPY . .

# Expose the port that your app uses (if any)
EXPOSE 8000

# Set the environment variable for the database URL
ENV DATABASE_URL=${DATABASE_URL}

# Run the command to start your app
CMD ["python", "src/main.py"]
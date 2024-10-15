# Dockerfile for FastAPI

# Base image: official Python image with version 3.9
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire FastAPI app to the container
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the app using Uvicorn as ASGI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

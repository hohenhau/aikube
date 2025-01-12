# Base image
FROM python:3.11-slim

# Set the working directory (Inside the Docker Container, not Locally!)
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the service port
EXPOSE 8000

# Set environment variable for the port
ARG INTERNAL_FASTAPI_PORT=8000
ENV INTERNAL_PORT=$INTERNAL_FASTAPI_PORT

# Start the FastAPI app
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $INTERNAL_PORT"]

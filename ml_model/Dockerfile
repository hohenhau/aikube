FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the service port
EXPOSE 5000

# Start the FastAPI app
CMD ["uvicorn", "model:app", "--host", "0.0.0.0", "--port", "5000"]

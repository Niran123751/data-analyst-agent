FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY ./app /app
COPY ./tests /tests

# Expose Render port (Render expects $PORT)
EXPOSE 10000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

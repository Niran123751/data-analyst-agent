FROM python:3.11-slim

WORKDIR /app

# Copy requirements.txt (must exist in build context!)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy source code
COPY ./app /app/app

EXPOSE 10000

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]

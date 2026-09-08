# Small, official Python base image
FROM python:3.12-slim

WORKDIR /app

# Copy only requirements first so Docker can cache this layer
# (dependencies rarely change; code changes often)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the actual application code
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

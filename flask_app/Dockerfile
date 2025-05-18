# Use an official Python runtime
FROM python:3.9-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies (like curl)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Define Flask app
ENV FLASK_APP=app

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
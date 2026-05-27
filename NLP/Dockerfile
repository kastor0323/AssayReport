# Use official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5002

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml first to leverage Docker build cache
COPY pyproject.toml /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir . || pip install --no-cache-dir pandas kiwipiepy nltk flask flask-cors beautifulsoup4 openpyxl lxml requests

# Pre-download NLTK data to ensure offline capability and instant startup
RUN python -m nltk.downloader -d /usr/local/share/nltk_data punkt stopwords averaged_perceptron_tagger

# Copy the rest of the application files
COPY . /app/

# Expose the service port
EXPOSE 5002

# Run the evaluator Flask application
CMD ["python", "resume_evaluator.py"]

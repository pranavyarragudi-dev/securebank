FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Environment variables
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV GUNICORN_WORKERS=3
ENV GUNICORN_THREADS=2

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health').raise_for_status()" || exit 1

# Start command with Gunicorn
CMD gunicorn --workers $GUNICORN_WORKERS \
             --threads $GUNICORN_THREADS \
             --bind 0.0.0.0:8080 \
             --access-logfile - \
             --error-logfile - \
             --log-level info \
             wsgi:app

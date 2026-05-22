# syntax=docker/dockerfile:1.7

# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install minimal runtime libraries used by image-processing wheels.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements-deploy.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip \
    && for attempt in 1 2 3 4 5; do \
        pip install --retries 10 --timeout 120 -r requirements-deploy.txt && break; \
        if [ "$attempt" = "5" ]; then exit 1; fi; \
        sleep 10; \
    done \
    && pip install --retries 10 --timeout 120 --no-deps ultralytics==8.3.40

# Copy application files
# Note: .dockerignore handles excluding large weights and training data
COPY web/ ./web/
COPY weights/best_yolo.pt ./weights/
COPY models/ ./models/

# Expose Streamlit port
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health', timeout=5)"

# Run the application
ENTRYPOINT ["streamlit", "run", "web/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

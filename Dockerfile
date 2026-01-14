# Hugging Face Spaces - Optimized Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start both FastAPI and Streamlit
# FastAPI on port 8000, Streamlit on port 7860 (HF Spaces default)
CMD uvicorn api.app:app --host 0.0.0.0 --port 8000 & \
    streamlit run streamlit_app/app.py --server.port 7860 --server.address 0.0.0.0

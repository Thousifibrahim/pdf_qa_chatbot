FROM python:3.9

# Set metadata
LABEL maintainer="Your Name <your.email@example.com>" \
      version="1.0.2" \
      description="PDF AI Assistant Streamlit App"

# Set environment variables for Streamlit
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    VIRTUAL_ENV=/app/venv

# Create non-root user for security
RUN groupadd -g 1005 appgroup && \
    useradd -u 1005 -g appgroup -m appuser && \
    mkdir -p /app/assets && \
    chown -R appuser:appgroup /app

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    libmupdf-dev \
    libfreetype6-dev \
    libblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt || { echo "pip install failed"; cat /app/requirements.txt; exit 1; }

# Copy application files
COPY app.py .
COPY qa_chain.py .
COPY document_processor.py .
COPY assets/ ./assets/

# Debug: Verify assets folder contents
RUN ls -la /app/assets

# Switch to non-root user
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# ==========================================

# Stage 1: Builder
# ==========================================
FROM python:3.11-slim AS builder

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /build

# Install compilation tools if needed for external packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker cache
COPY app/requirements.txt .

# Install dependencies to a target prefix folder
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ==========================================
# Stage 2: Final Runtime
# ==========================================
FROM python:3.11-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Create a secure, non-privileged system user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /sbin/nologin appuser

# Set runtime working directory
WORKDIR /home/appuser/app

# Copy installed site-packages from the builder
COPY --from=builder /install /usr/local

# Copy application files
COPY app/ ./app/
COPY .env* ./

# Set proper permissions for the non-root user
RUN chown -R appuser:appgroup /home/appuser/app

# Switch to the non-root user
USER appuser

# Expose port
EXPOSE 8000

# Native Python-based healthcheck to avoid installing curl (minimizes CVE attack surface)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=3)" || exit 1

# Launch the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

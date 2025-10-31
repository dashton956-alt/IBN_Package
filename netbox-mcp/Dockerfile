FROM python:3.13-slim

# Keep stdout/stderr unbuffered
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Build args: repo to clone and optional ref
ARG REPO_URL=https://github.com/netboxlabs/netbox-mcp-server.git
ARG REPO_REF=main

# Install minimal build deps and git for cloning
RUN apt-get update \
    && apt-get install -y --no-install-recommends git build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Clone the repo into /app (shallow)
RUN git clone --depth 1 --branch ${REPO_REF} ${REPO_URL} /app/src \
    || (echo "Failed to clone ${REPO_URL}@${REPO_REF}" && exit 1)

WORKDIR /app/src

# Install runtime dependencies directly (avoid building a wheel from the
# repository because the upstream project uses a flat layout that can cause
# setuptools to error during wheel build). We install the explicit runtime
# deps from pyproject.toml and uvicorn.
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir "httpx>=0.28.1" "fastmcp>=2.12.0,<2.13" \
    "requests>=2.31.0" "pydantic>=2.0" "pydantic-settings>=2.0" \
    && pip install --no-cache-dir "uvicorn[standard]"

# Expose the HTTP transport default port (can be overridden via PORT env)
EXPOSE 8002

# Default environment variables (can be overridden at runtime)
ENV TRANSPORT=http \
    HOST=0.0.0.0 \
    PORT=8002 \
    VERIFY_SSL=true \
    LOG_LEVEL=INFO

# Default start command (can be overridden). The project expects server.py at
# repo root; uv is used in upstream docs so we use that as default.
CMD ["python", "server.py"]

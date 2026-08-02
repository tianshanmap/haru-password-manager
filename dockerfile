# --- Stage 1: Build the virtual environment ---
FROM python:3.12-slim-bookworm AS builder

# Install uv by copying it directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Optimize uv for container builds
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Copy dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies only (avoids re-installing on code changes)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application code
COPY . .

# Sync the entire project (installs your local project code into the venv)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# --- Stage 2: Run the application ---
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

# Copy the pre-built virtual environment and app code from the builder stage
COPY --from=builder /app /app

# Place the virtual environment at the front of the PATH variable
ENV PATH="/app/.venv/bin:$PATH"

# Expose your application port (change 8000 to match your app)
EXPOSE 8000

# Run your application (Example assumes a FastAPI/Uvicorn entry point)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

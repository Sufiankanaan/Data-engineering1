FROM python:3.13-slim

WORKDIR /code

ENV PATH="/code/.venv/bin:$PATH"

# Bring in the uv binary from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Install dependencies first (better layer caching)
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked

# Copy the application code
COPY pipeline.py pipeline.py

ENTRYPOINT ["python", "pipeline.py"]
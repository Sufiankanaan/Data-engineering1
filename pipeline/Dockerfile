FROM python:3.11-slim

WORKDIR /code

ENV PATH="/code/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/


COPY "pyproject.toml" "uv.lock" ".python-version" ./

RUN uv sync --locked

COPY pipeline.py pipeline.py

ENTRYPOINT ["python", "pipeline.py"]
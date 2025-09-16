FROM python:3.13-slim
ENV UV_SYSTEM_PYTHON=1
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.8.17 /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev
COPY src/ .
EXPOSE 8008
CMD ["uv", "run", "uvicorn", "answerer.app:app", "--host", "0.0.0.0", "--port", "8008"]

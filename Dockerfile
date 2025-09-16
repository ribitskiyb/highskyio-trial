FROM python:3.13-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.8.17 /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --locked
COPY src/* .
EXPOSE 8008
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8008"]

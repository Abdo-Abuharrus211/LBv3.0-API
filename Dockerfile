FROM python:3.13-slim

WORKDIR /usr/src/app

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .

COPY . .

# Install only project dependencies
RUN uv sync --no-dev

EXPOSE 8000
CMD ["uv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
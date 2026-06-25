FROM python:3.14
LABEL authors="ABDULQADIR ABUHARRUS"
WORKDIR /usr/src/app

RUN pip install uv
# tell uv to use the image's Python not its own
ENV UV_SYSTEM_PYTHON=1
ENV PYTHONUNBUFFERED=1
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

COPY . .
EXPOSE 8000
CMD ["uv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
FROM python:3.11.2-slim

WORKDIR /code

COPY pyproject.toml /code/pyproject.toml

RUN apt-get update && apt-get install -yq \
    build-essential \
    curl

ENV POETRY_VIRTUALENVS_CREATE false
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN /root/.local/bin/poetry install --no-root --only main

COPY app /code/app

RUN chown -R www-data:www-data /code

USER www-data
EXPOSE 8000
ENV PYTHONPATH "/code"
ENV APP_DATA_STORAGE "/code/app/data"

CMD ["uvicorn", "app.src.fastapi.api:app", "--host", "0.0.0.0", "--port", "8000"]

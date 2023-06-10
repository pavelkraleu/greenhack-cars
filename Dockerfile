FROM python:3.11-slim

ENV PORT=8080
ENV PYTHONUNBUFFERED True
ENV DJANGO_SETTINGS_MODULE cars.settings.local

WORKDIR /app

RUN apt-get update && apt-get -y install libpq-dev gcc binutils libproj-dev gdal-bin && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app
COPY poetry.lock /app
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /app

EXPOSE 8080

CMD ["./entrypoint.sh"]
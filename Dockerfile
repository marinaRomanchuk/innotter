FROM python:3.9 AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VERSION=1.1.13 \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  PYSETUP_PATH="/app" \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction

# Creating folders, and files for a project:
COPY . /code
RUN ["chmod", "+x", "./entrypoint.sh"]

ENTRYPOINT ["sh", "./entrypoint.sh"]

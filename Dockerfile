FROM python:3.9
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.

# Install poetry
RUN pip3 install poetry

# Copy in the config files
COPY pyproject.toml poetry.lock ./

# Install only dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

# Copy in everything else and install
COPY  ./crawler /crawler
WORKDIR /crawler
RUN poetry install --no-dev

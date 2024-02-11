FROM python:3.11.7

# Set the working directory in the container
WORKDIR /opt/project

# Setup environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /opt/project

# Install dependencies
RUN set -xe \
		&& apt-get update \
		&& apt-get install -y --no-install-recommends build-essential python3-dev default-libmysqlclient-dev\
		&& pip install --no-cache-dir virtualenvwrapper poetry==1.7.0 \
		&& apt-get clean \
		&& rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY [ "poetry.toml", "poetry.lock", "pyproject.toml", "./" ]
RUN poetry install --no-root --no-dev
RUN poetry run pip install django-admin-honeypot-updated-2021

# Copy project files
COPY src src

# Expose Django development server port
EXPOSE 8000

# Set up entrypoint
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

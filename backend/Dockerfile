FROM python:3.14-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev python3-pip curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"
ENV UV_NO_DEV=1

WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY pyproject.toml uv.lock /app/

# Install dependencies
RUN uv sync --locked --group prod

# Copy the current directory contents into the container at /app
COPY website /app
COPY resources/entrypoint.sh /

ENV DJANGO_SETTINGS_MODULE="drankspel.settings.production"

ENV DJANGO_STATIC_ROOT="/static"
ENV DJANGO_MEDIA_ROOT="/media"
ENV DJANGO_LOG_ROOT="/log"

RUN mkdir -p $DJANGO_STATIC_ROOT
RUN mkdir -p $DJANGO_MEDIA_ROOT
RUN mkdir -p $DJANGO_LOG_ROOT

ENV DJANGO_STATIC_URL="/static/"
ENV DJANGO_MEDIA_URL="/media/"

RUN touch /log/django.log

RUN uv run manage.py collectstatic --noinput

RUN chown -R nobody:nogroup $DJANGO_MEDIA_ROOT
RUN chown -R nobody:nogroup /log/django.log

EXPOSE 80

# Command to run uWSGI
CMD ["/bin/sh", "/entrypoint.sh"]

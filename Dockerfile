# define an alias for the specific python version used in this file.
FROM docker.io/python:3.12.6-slim-bookworm AS python

# Python build stage
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=production

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev

COPY ./requirements.txt .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r requirements.txt

# Python 'run' stage
FROM python AS python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV BUILD_ENV=${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# ✅ CORREÇÃO: Criar diretórios ANTES do usuário
RUN mkdir -p ${APP_HOME}/staticfiles ${APP_HOME}/media

# ✅ CORREÇÃO: Criar usuário com diretório home
RUN groupadd --system django && \
    useradd --system --create-home --gid django django && \
    chown -R django:django ${APP_HOME}

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq-dev \
  gettext \
  netcat-traditional \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# ✅ CORREÇÃO: Converter quebras de linha Windows para Unix
COPY ./compose/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

COPY ./compose/django/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

COPY ./compose/django/start-dev /start-dev
RUN sed -i 's/\r$//g' /start-dev && chmod +x /start-dev

COPY ./compose/django/start-celeryworker /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker && chmod +x /start-celeryworker

COPY ./compose/django/start-celerybeat /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat && chmod +x /start-celerybeat

# Copy application code to WORKDIR
COPY --chown=django:django . ${APP_HOME}

# ✅ CORREÇÃO: Dar permissões completas nos diretórios de trabalho
RUN chmod -R 755 ${APP_HOME} && \
    chown -R django:django ${APP_HOME}

USER django

ENTRYPOINT ["/entrypoint"]
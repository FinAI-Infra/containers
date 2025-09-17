ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

ARG APP_USER=compass
ARG APP_DIR=/app

RUN set -e; \
    apt-get update; \
    apt-get install -y --no-install-recommends build-essential git; \
    useradd --create-home $APP_USER; \
    mkdir -p $APP_DIR; \
    chown -R $APP_USER:$APP_USER $APP_DIR;

ENV VIRTUAL_ENV="$APP_DIR/.venv"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

USER $APP_USER
WORKDIR $APP_DIR
COPY --chown=$APP_USER:$APP_USER . .
RUN set -e; \
    python -m venv .venv; \
    pip install --no-cache -r requirements.txt;

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim-bookworm

ARG GITHUB_SHA
ARG GITHUB_SHA_SHORT
ARG BUILD_DATE
ARG APP_USER=compass
ARG APP_DIR=/app

LABEL org.opencontainers.image.revision=$GITHUB_SHA \
      org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.version=$GITHUB_SHA_SHORT \
      org.opencontainers.image.source="https://github.com/FinAI-Infra/containers/tree/main/compass-runtime"

ENV TZ=Asia/Singapore
ENV RUNTIME_VERSION=$GITHUB_SHA_SHORT
ENV VIRTUAL_ENV="$APP_DIR/.venv"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN set -e; \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends tzdata git make curl rsync; \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime; \
    echo $TZ > /etc/timezone; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*; \
    useradd --create-home $APP_USER; \
    ln -s $APP_DIR/bin/sync-entrypoint.sh /home/$APP_USER/sync-entrypoint.sh; \
    git config --system --add safe.directory '*'

COPY --from=builder $APP_DIR $APP_DIR

USER $APP_USER
WORKDIR $APP_DIR
ENTRYPOINT ["/app/bin/entrypoint.sh"]

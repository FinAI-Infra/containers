FROM python:3.13-alpine

ARG GITHUB_SHA
ARG GITHUB_SHA_SHORT
ARG BUILD_DATE
ARG APP_USER=app
ARG APP_DIR=/app

LABEL org.opencontainers.image.revision=$GITHUB_SHA \
      org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.version=$GITHUB_SHA_SHORT \
      org.opencontainers.image.source="https://github.com/FinAI-Infra/containers/tree/main/github-token-manager"

RUN set -e; \
    apk update; \
    apk upgrade; \
    apk cache clean; \
    adduser -D -h $APP_DIR $APP_USER;

USER $APP_USER
WORKDIR $APP_DIR
COPY --chown=$APP_USER:$APP_USER *.py requirements.txt .

ENV VIRTUAL_ENV="${APP_DIR}/.venv"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN set -e; \
    python -m venv .venv; \
    pip install --no-cache -r requirements.txt;

CMD ["python", "main.py"]

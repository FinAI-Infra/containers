FROM python:3.13-alpine

ARG GITHUB_SHA
ARG GITHUB_SHA_SHORT
ARG BUILD_DATE

LABEL org.opencontainers.image.revision=$GITHUB_SHA \
      org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.version=$GITHUB_SHA_SHORT \
      org.opencontainers.image.source="https://github.com/FinAI-Infra/containers/tree/main/github-token-manager"

WORKDIR /app

COPY *.py requirements.txt .

ENV VIRTUAL_ENV="/app/.venv"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN set -e; \
    python -m venv .venv; \
    pip install --no-cache -r requirements.txt;

CMD ["python", "/app/main.py"]

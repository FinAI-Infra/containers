ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim-bookworm

ARG GITHUB_SHA
ARG GITHUB_SHA_SHORT
ARG BUILD_DATE
ARG PYTORCH_VERSION=2.6.0

LABEL org.opencontainers.image.revision=$GITHUB_SHA \
      org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.version=$GITHUB_SHA_SHORT \
      org.opencontainers.image.source="https://github.com/FinAI-Project/compass-ci"

ENV TZ=Asia/Singapore
ENV RUNTIME_VERSION=$GITHUB_SHA_SHORT
ENV VIRTUAL_ENV="/workspace/.venv"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /workspace
COPY *.sh torch-$PYTORCH_VERSION/requirements.txt .
RUN set -e; \
    apt update; \
    apt install -y --no-install-recommends build-essential tzdata git make curl wget unzip openssh-server; \
    curl -o awscliv2.zip https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip; \
    unzip awscliv2.zip; \
    ./aws/install; \
    rm -rf aws awscliv2.zip; \
    wget -qO- cli.runpod.net | bash; \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime; \
    echo $TZ > /etc/timezone; \
    python -m venv .venv; \
    pip install --no-cache -r requirements.txt; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*;

EXPOSE 22

ENTRYPOINT ["/workspace/start.sh"]
CMD ["sleep", "infinity"]

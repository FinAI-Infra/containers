FROM ghcr.io/actions/actions-runner

ARG GITHUB_SHA
ARG GITHUB_SHA_SHORT
ARG BUILD_DATE

LABEL org.opencontainers.image.revision=$GITHUB_SHA \
      org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.version=$GITHUB_SHA_SHORT \
      org.opencontainers.image.source="https://github.com/FinAI-Infra/containers/tree/main/actions-runner"

RUN set -e; \
    sudo apt-get update; \
    sudo apt-get upgrade -y; \
    sudo apt-get install -y --no-install-recommends build-essential; \
    sudo sed -i 's/\(archive\|security\)\.ubuntu\.com/azure.archive.ubuntu.com/g' /etc/apt/sources.list; \
    sudo apt-get clean; \
    sudo rm -rf /var/lib/apt/lists/*;

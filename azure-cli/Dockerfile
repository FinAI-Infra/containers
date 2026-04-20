# https://mcr.microsoft.com/en-us/artifact/mar/azure-cli
FROM mcr.microsoft.com/azure-cli:azurelinux3.0
LABEL org.opencontainers.image.description="Used for data synchronization tasks" \
      ai.fenghe.k8s.usage='{"cluster":"fengheai-k8s","cronjobs":["apps/output-sync","arc-system/fds-data-sync"]}'
RUN set -e; \
    tdnf update -y; \
    tdnf install -y tar util-linux azcopy; \
    tdnf clean all; \
    rm -rf /var/cache/tdnf/* /tmp/*; \
    tar --version; \
    od --version; \
    azcopy --version;

FROM alpine

ARG GITHUB_SHA
ARG GITHUB_SHA_SHORT
ARG BUILD_DATE

LABEL org.opencontainers.image.revision=$GITHUB_SHA \
      org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.version=$GITHUB_SHA_SHORT \
      org.opencontainers.image.source="https://github.com/FinAI-Infra/containers/tree/main/git-tools"

WORKDIR /app

COPY *.sh /app

RUN set -e; \
    apk add --no-cache curl openssl git jq; \
    rm -rf /var/cache/apk/*; \
    chmod a+x *.sh; \
    git config --global credential.helper '/app/git-credential-helper.sh'; \
    git config --global --add safe.directory /app/code;

CMD ["/app/github-clone.sh"]
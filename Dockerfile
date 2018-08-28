FROM python:3.6-alpine3.7
LABEL maintainer "Kazuya Takei"
ARG YAGURA_VERSION=0.6.0

# Install Yagura with dependencies from PyPI
RUN apk add --no-cache gcc musl-dev && \
    pip install "yagura==${YAGURA_VERSION}" && \
    apk del gcc  musl-dev

# MySQL (flagged only)
ARG USE_MYSQLCLIENT=0
RUN if [ "${USE_MYSQLCLIENT}" = "1" ]; then \
        apk add --no-cache mariadb-client-libs mariadb-dev gcc musl-dev; \
        pip install --no-cache-dir mysqlclient; \
        apk del mariadb-dev gcc musl-dev; \
        fi

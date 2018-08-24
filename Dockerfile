FROM python:3.6-alpine3.7
LABEL maintainer "Kazuya Takei"
ARG YAGURA_VERSION=0.6.0

# Install Yagura from PyPI
RUN pip install "yagura==${YAGURA_VERSION}"

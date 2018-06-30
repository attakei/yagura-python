FROM python:3.6-alpine
LABEL maintainer "Kazuya Takei"

COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

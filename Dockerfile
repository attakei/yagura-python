FROM python:3.6-alpine3.7
LABEL maintainer "Kazuya Takei"

# System
RUN mkdir /app
WORKDIR /app

# PyPI Package installation
COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY ./ /app/

RUN apk add --no-cache --update gettext \
    && python manage.py compilemessages

# Run settings
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=yagura.settings.env
ENTRYPOINT ["sh", "/app/bin/entry-point.sh"]
CMD ["web"]

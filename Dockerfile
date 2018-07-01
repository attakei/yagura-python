FROM python:3.6-alpine
LABEL maintainer "Kazuya Takei"

# System
RUN addgroup -g 1000 app \
    && adduser -G app -u 1000 -D -h /home/app app \
    && mkdir /app \
    && chown app:app /app
RUN apk add --no-cache sudo busybox-suid \
	&& echo 'app ALL=(ALL) NOPASSWD: /usr/sbin/crond' > /etc/sudoers.d/app
USER app
WORKDIR /app

# PyPI Package installation
COPY ./requirements.txt /tmp/
RUN pip install --user -r /tmp/requirements.txt
COPY --chown=app:app ./ /app/

# Run settings
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=yagura.settings.env
CMD sh /app/bin/entry-point.sh

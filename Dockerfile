FROM python:3.6-alpine
LABEL maintainer "Kazuya Takei"

# System
RUN addgroup -g 1000 app \
    && adduser -G app -u 1000 -D -h /home/app app \
    && mkdir /app \
    && chown app:app /app
USER app
WORKDIR /app

# PyPI Package installation
COPY ./requirements.txt /tmp/
RUN pip install --user -r /tmp/requirements.txt
COPY ./ /app/

# Run settings
EXPOSE 8000
CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]

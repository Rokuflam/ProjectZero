FROM python:3.12-alpine3.17
LABEL maintainer="kulibabaroman6@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./scripts /scripts

WORKDIR /usr/src/backend
COPY ./backend .
COPY pyproject.toml .
COPY poetry.lock .
EXPOSE 8000

RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    pip install poetry pylint && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    addgroup -g 1001 django-group && \
    adduser \
        --disabled-password \
        --no-create-home \
        --uid 1001 \
        --ingroup django-group \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-group /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["dev.entrypoint.sh"]

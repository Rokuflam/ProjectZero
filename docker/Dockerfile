FROM python:3.12-alpine3.17
LABEL maintainer="roman.kulibaba@wesoftyou.com"

ENV PYTHONUNBUFFERED 1

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

COPY ./scripts /scripts
COPY ./backend /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install poetry && \
    /py/bin/poetry config virtualenvs.create false && \
    /py/bin/poetry install --no-dev && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["entrypoint.sh"]
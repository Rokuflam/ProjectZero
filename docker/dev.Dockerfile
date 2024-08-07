FROM ubuntu
FROM python:3.12-alpine3.17
LABEL maintainer="kulibabaroman6@gmail.com"
ARG UID
ARG GID

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update the package list, install sudo, create a non-root user, and grant password-less sudo permissions
RUN apt update && \
    apt install -y sudo && \
    addgroup --gid $GID nonroot && \
    adduser --uid $UID --gid $GID --disabled-password --gecos "" nonroot && \
    echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

# Set the non-root user as the default user
USER nonroot

WORKDIR /home/nonroot/app
COPY --chown=nonroot:nonroot . /home/nonroot/app
RUN chmod -R 755 /home/nonroot/app

COPY ./scripts /scripts

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

CMD ["dev.entrypoint.sh"]
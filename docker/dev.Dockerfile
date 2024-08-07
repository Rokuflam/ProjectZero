FROM python:3.12-alpine3.17
LABEL maintainer="kulibabaroman6@gmail.com"

# Create a new user with a specific UID and GID
ARG USER_ID
ARG GROUP_ID
RUN groupadd -g $GROUP_ID customuser && \
    useradd -u $USER_ID -g $GROUP_ID -m customuser

# Switch to the new user
USER customuser

# Set the working directory
WORKDIR /home/customuser

# Copy the application files to the container
COPY . /home/customuser

# Ensure the customuser owns the application files
RUN chown -R customuser:customuser /home/customuser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

CMD ["dev.entrypoint.sh"]

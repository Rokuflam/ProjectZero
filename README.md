# ProjectZero


A DRF project to start new projects faster and better.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Acknowledgments](#acknowledgments)

## Tutorials

### Environment set-up
- [Development set-up using Terraform](tutorials/dev-terraform.md)
- [Development set-up using AWS Console](tutorials/dev-aws-ui.md)

## Features

- Django 5+
- Django REST Framework for building APIs
- User authentication and authorization
- Social authentication
- Token-based authentication
- Serialization of models
- CRUD operations
- Testing with `unittest`
- Continuous Integration with GitHub Actions
- Linting using Pylint
- Sending email with Anymail
- HealthCheckMiddleware
- SQLProfilerMiddleware

## Prerequisites

Make sure you have the following installed on your machine:

- Docker
- Python 3.12
- pip
- poetry (optional but recommended)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Rokuflam/ProjectZero.git
    ```

2. Navigate to the project directory:

    ```bash
    cd ProjectZero
    ```
   If you are using Pycharm, [follow documentation to set up poetry env](https://www.jetbrains.com/help/pycharm/poetry.html), otherwise follow next steps

3. Open Poetry shell:

    ```bash
    poetry shell
    ```

4. Generate Poetry lock file

   ```bash
    poetry lock
   ```

5. Install or Update project dependencies:

    ```bash
    poetry install
    ```
    ```bash
    poetry update
    ```

## Configuration

1. Create a copy of the `.env.example` file and name it `.env`. Update the values as needed.

2. If you need a Social Auth, go to `backend/apps/user/fixtures/social-auth.json`,
and change client_id for the app you are about to use.

3. If you need Anymail, fill variables from example.env into your env file,
and choose `EMAIL_BACKEND` in `backend/config/settings/{env you use}.py`

## Usage
- Run the development server:
    ```bash
    docker-compose -f docker/docker-compose-local.yml up
    ```

- Run tests
    ```bash
    docker-compose -f docker/docker-compose-local.yml run --rm app sh -c "python manage.py test apps"
    ```

- Pylint check
    ```bash
    docker-compose -f docker/docker-compose-local.yml run --rm app sh -c "pylint apps --rcfile=.pylintrc"
    ```

## API Documentation

1.   [Swagger](http://localhost:8000/api/docs/) /api/docs/
2.   [Admin panel](http://localhost:8000/admin/) /admin/

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/)
- [Sentry](https://docs.sentry.io/)
- [Pylint](https://pypi.org/project/pylint/)
- [Anymail](https://anymail.dev/en/)
- [Django Extensions](https://pypi.org/project/django-extensions/)
- [Terraform](https://www.terraform.io/)

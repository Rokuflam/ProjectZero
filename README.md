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

## Features

- Django 5.0+
- Django REST Framework for building APIs
- User authentication and authorization
- Token-based authentication
- Serialization of models
- CRUD operations
- Testing with `unittest`
- Continuous Integration with GitHub Actions
- Linting using Pylint

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


## Usage
- Run the development server:
    ```bash
    docker-compose -f docker/docker-compose-local.yml start
    ```

- Run tests
    ```bash
    docker-compose -f docker/docker-compose-local.yml run --rm app sh -c "python manage.py test apps"
    ```

- Pylint check
    ```bash
    docker-compose -f docker/docker-compose-local.yml run --rm app sh -c "pylint --rcfile=.pylintrc .\apps\"
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

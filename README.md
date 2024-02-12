# ProjectZero

[![Build Status](https://travis-ci.org/your-username/django-rest-project.svg?branch=master)](https://app.travis-ci.com/github/Rokuflam/ProjectZero)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A DRF project to start new projects faster and better.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- Django 5.0+
- Django REST Framework for building APIs
- User authentication and authorization
- Token-based authentication
- Serialization of models
- CRUD operations
- Testing with `unittest`
- Continuous Integration with GitHub Actions

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

1. Run the development server:
    ```bash
    docker-compose -f docker/docker-compose-local.yml start
    ```

## API Documentation

1.   [Swagger](http://localhost:8000/api/docs/) /api/docs/
2.   [Admin panel](http://localhost:8000/admin/) /admin/


## Contributing
Thank you for considering contributing to ProjectZero!
We welcome contributions from the community to make this project better.
Please take a moment to review this document to understand how to contribute effectively.

### Purpose
ProjectZero aims to provide a foundation for building Django REST
Framework projects efficiently. Your contributions can help enhance features,
improve documentation, fix bugs, and more.

### Code of Conduct
Please note that this project is released with a Code of Conduct.
By participating in this project, you agree to abide by its terms.

### How to Contribute
We appreciate various forms of contributions, including bug reports,
feature requests, documentation improvements, and code contributions.
Before you start, consider searching the issues and pull requests
to see if someone else is already working on or has reported the same issue.

### Getting Started
1. Fork the repository.

2. Clone your forked repository to your local machine:

   ```bash
   git clone https://github.com/your-username/ProjectZero.git
   ```
3. Create a new branch for your contribution:

   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Install the necessary dependencies and set up your development environment as
described in the Installation and Configuration sections.

### Pull Request Guidelines
1. Ensure your code adheres to the coding standards and style of the project.
2. Write clear and concise commit messages.
3. Provide a detailed description of your changes in your pull request.
4. Run tests locally to ensure your changes do not introduce new issues.
5. Rebase your branch on the latest main branch before submitting the pull request.

### Issue Guidelines
If you encounter any issues or have feature requests,
please open an issue with a clear and descriptive title
and provide as much information as possible to help us understand and address the problem.

### Review Process
All contributions will be reviewed by the maintainers.
Constructive feedback may be provided to improve the quality of the contributions. Once approved, your changes will be merged into the main branch.

### Contact Information
If you have any questions or need assistance,
feel free to reach out to the maintainers via kulibabaroman6@gmail.com 
or open a GitHub issue.

We appreciate your contributions to ProjectZero!
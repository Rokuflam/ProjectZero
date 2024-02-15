from rest_framework.exceptions import APIException


class UserAlreadyExistsException(APIException):
    status_code = 409  # HTTP status code for conflict
    default_detail = 'User already exists'
    default_code = 'user_exists'

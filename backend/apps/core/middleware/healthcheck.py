"""
This module contains the HealthCheckMiddleware class for Django applications.
It is designed to handle health check requests by performing necessary health checks
 and returning the status of the application.

Classes:
    HealthCheckMiddleware: A middleware class for intercepting requests to the health check endpoint and
    performing health checks.

Usage:
    To use this middleware, add it to the MIDDLEWARE setting in your Django project's settings.py file.
    Ensure that the health check endpoint ('/health/') is configured in your URLconf
     if it is not handled by the middleware itself.
"""
from django.conf import settings
from django.http import JsonResponse


class HealthCheckMiddleware:
    """
    Middleware class for performing health checks on the application.
    """

    def __init__(self, get_response):
        """
        Initialize a new instance of the class.

        :param get_response: The response handler function to be called.
        :type get_response: function
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        The __call__ method is used to handle incoming requests.

        Parameters:
            request (HttpRequest): The incoming HttpRequest object.

        Returns:
            HttpResponse: The HttpResponse object generated by the view function.

        Raises:
            None.

        Example:

        >>> request = HttpRequest()
        >>> response = self.__call__(request)
        >>> print(response)
        <HttpResponse object>
        """
        if request.path == settings.HEALTH_CHECK_URL:
            return self.perform_health_checks()
        return self.get_response(request)

    @staticmethod
    def perform_health_checks():
        """
            Method Name: perform_health_checks

            Description:
                This method performs various health checks for the application
                and returns the result as a JsonResponse.

            Returns:
                JsonResponse: The health check result as a JSON response.
        """
        # Put all health check logic here
        data = {"status": "OK", "message": "Application is running!"}
        return JsonResponse(data)
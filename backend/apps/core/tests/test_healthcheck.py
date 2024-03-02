"""
This test module contains unit tests for the HealthCheckMiddleware class
"""
import unittest
from django.http import HttpRequest, JsonResponse
from django.conf import settings
from apps.core.middleware.healthcheck import HealthCheckMiddleware


class TestHealthCheckMiddleware(unittest.TestCase):
    """
    This class provides a suite of unit tests for the HealthCheckMiddleware component of a Django app.
    """
    def setUp(self):
        """
        Set up for the tests.
        """

        # Define a dummy get_response function that returns None
        def dummy_get_response(request):  # pylint: disable=unused-argument
            return None

        # Using the dummy function as the get_response for the middleware
        self.middleware = HealthCheckMiddleware(dummy_get_response)

    def test_init(self):
        """
        Test __init__ method of HealthCheckMiddleware.
        """
        self.assertTrue(callable(self.middleware.get_response))

    def test_call_with_health_check_url(self):
        """
        Test __call__ method of HealthCheckMiddleware when request url is health check url.
        """
        request = HttpRequest()
        request.path = settings.HEALTH_CHECK_URL
        response = self.middleware.__call__(request)  # pylint: disable=unnecessary-dunder-call
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(
            response.content.decode(),
            JsonResponse({"status": "OK", "message": "Application is running!"}).content.decode()
        )

    def test_call_with_non_health_check_url(self):
        """
        Test __call__ method of HealthCheckMiddleware when request url is not health check url.
        """
        request = HttpRequest()
        request.path = '/non-health-check/url'
        response = self.middleware.__call__(request)  # pylint: disable=unnecessary-dunder-call
        self.assertIsNone(response)

    def test_perform_health_checks(self):
        """
        Test perform_health_checks method of HealthCheckMiddleware.
        """
        response = self.middleware.perform_health_checks()
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(
            response.content.decode(),
            JsonResponse({"status": "OK", "message": "Application is running!"}).content.decode()
        )

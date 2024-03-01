"""
This module contains unit tests for the `anymail` module's email sending functionalities
 within a Django application. It covers tests for sending both plain text and HTML emails,
 including scenarios where emails are sent successfully, where bad headers are provided,
 and where exceptions are encountered during the email sending process.

Usage:
To run these tests, ensure that Django's test runner is configured for your project,
 and execute the test suite through Django's manage.py test command.
"""
import unittest
from unittest.mock import patch
from django.core.mail import (
    BadHeaderError,
    EmailMultiAlternatives
)
from django.http import HttpResponse
from apps.core.utils import anymail


class TestAnymail(unittest.TestCase):
    """
    TestAnymail
    class is a unit test class that tests the functionality of the send_email function in the anymail module.
    """
    def setUp(self):
        self.subject = "Test email"
        self.message = "This a test email"
        self.from_email = "test@example.com"
        self.recipient_list = ["recipient@example.com"]

    @patch('apps.core.utils.anymail.send_mail')
    def test_send_email_success(self, mock_send):
        """Test send_email function with successful email"""
        mock_send.return_value = 'Test email sent'
        result = anymail.send_email(self.subject, self.message, self.from_email, self.recipient_list)
        self.assertIsInstance(result, HttpResponse)
        self.assertIn("Email sent successfully", result.content.decode())

    @patch('apps.core.utils.anymail.send_mail')
    def test_send_email_bad_header(self, mock_send):
        """Test send_email function with BadHeaderError"""
        mock_send.side_effect = BadHeaderError
        self.message += " with bad header"
        self.subject += " with bad header"
        result = anymail.send_email(self.subject, self.message, self.from_email, self.recipient_list)
        self.assertIsInstance(result, HttpResponse)
        self.assertIn("Error in email header", result.content.decode())

    @patch('apps.core.utils.anymail.send_mail')
    def test_send_email_exception(self, mock_send):
        """Test send_email function with general Exception"""
        mock_send.side_effect = Exception
        self.message += " causing exception"
        self.subject += " causing exception"
        result = anymail.send_email(self.subject, self.message, self.from_email, self.recipient_list)
        self.assertIsInstance(result, HttpResponse)
        self.assertIn("Error sending email", result.content.decode())


class TestSendEmailFromHTML(unittest.TestCase):
    """

    Class: TestSendEmailFromHTML

    The TestSendEmailFromHTML class is a unit test class that tests the functionality of the"""
    def setUp(self):
        """
        Sets up the necessary variables for testing the method.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        self.subject = "Test Subject"
        self.html_content = "<html><body><h1>Test Content</h1></body></html>"
        self.from_email = "test@example.com"
        self.recipient_list = ["recipient1@example.com", "recipient2@example.com"]
        self.text_content = "Test Text Content"

    def test_send_email_from_html_success(self):
        """
        Test case for the send_email_from_html_success method.
        """
        response = anymail.send_email_from_html(
            self.subject,
            self.html_content,
            self.from_email,
            self.recipient_list,
            self.text_content
        )
        self.assertIsInstance(response, HttpResponse)
        self.assertIn(b"Email sent successfully.", response.content)

    def test_send_email_from_html_without_text_content(self):
        """
        Method to test the functionality of sending an email from HTML without text content.
        """
        response = anymail.send_email_from_html(
            self.subject,
            self.html_content,
            self.from_email,
            self.recipient_list
        )
        self.assertIsInstance(response, HttpResponse)
        self.assertIn(b"Email sent successfully.", response.content)

    def test_send_email_from_html_failure(self):
        """
        Test the behavior of send_email_from_html function when
        EmailMultiAlternatives.send raises an exception.
        """
        with unittest.mock.patch.object(EmailMultiAlternatives, 'send', side_effect=Exception("Test error")):
            response = anymail.send_email_from_html(
                self.subject,
                self.html_content,
                self.from_email,
                self.recipient_list,
                self.text_content
            )
            self.assertIsInstance(response, HttpResponse)
            self.assertIn(b"Error sending email:", response.content)

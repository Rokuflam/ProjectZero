"""
This module provides functions to send emails using Django's email utilities.
 It includes both plain text and HTML email sending capabilities,
 encapsulating the functionality within a simplified API for ease of use in Django projects.

Functions:
- send_email: Sends a simple plain text email.
- send_email_from_html: Sends an email with HTML content,
 optionally including a plain text version for email clients that do not support HTML.

Both functions aim to abstract the complexities of sending emails with Django,
 handling errors gracefully and providing a clear interface for developers.
 The module demonstrates how to use Django's built-in `send_mail` and `EmailMultiAlternatives`
 for email sending tasks, catering to a wide range of email content types.

Example Usage:
    from email_sending_module import send_email, send_email_from_html

    # Sending a plain text email
    send_email("Test Subject", "This is the body of the email.", "from@example.com", ["to@example.com"])

    # Sending an HTML email with a fallback plain text version
    send_email_from_html(
    "Test Subject", "<html><body><h1>HTML Content</h1></body></html>", "from@example.com", ["to@example.com"]
    )

Note:
- These functions are designed for use within Django projects
 and require Django's EMAIL_BACKEND to be properly configured.
- Error handling is implemented to catch and respond to common issues such as bad header errors.
"""
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.utils.html import strip_tags


def send_email(subject, message, from_email, recipient_list):
    """Sends an email with the provided subject, message, and sender and recipient email addresses.

    Parameters:
        subject (str): The subject of the email.
        message (str): The content of the email.
        from_email (str): The sender's email address.
        recipient_list (list[str]): A list of recipient email addresses.

    Returns:
        HttpResponse: indicating whether the email was sent successfully
         or an error occurred during the process.
    """
    try:
        result = send_mail(subject, message, from_email, recipient_list)
        return HttpResponse(f"Email sent successfully. Result: {result}")
    except BadHeaderError as e:
        return HttpResponse(f"Error in email header: {e}")
    except Exception as e:
        return HttpResponse(f"Error sending email: {e}")


def send_email_from_html(subject, html_content, from_email, recipient_list, text_content=None):
    """
    Send an email with HTML content.

    Parameters:
    - subject (str): The subject of the email.
    - html_content (str): The HTML content of the email.
    - from_email (str): The sender's email address.
    - recipient_list (list): A list of recipient email addresses.
    - text_content (str, optional): The plain text content of the email.
     If not provided, a simple 'strip_tags' conversion of the HTML content will be used as fallback.

    Returns:
    - HttpResponse: A response indicating the result of the email sending.

    Example usage:
    send_email_from_html(
    "Hello", "<html><body><h1>Welcome</h1></body></html>", "sender@example.com", ["recipient@example.com"]
    )

    Note: This method requires the 'django.utils.html' module to be imported.

    """
    try:
        # If no plain text content is provided, use a simple strip_tags as fallback
        if not text_content:
            text_content = strip_tags(html_content)

        # Create an instance of EmailMultiAlternatives
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")  # Attach the HTML version
        result = msg.send()  # Send the email
        return HttpResponse(f"Email sent successfully. Result: {result}")
    except Exception as e:
        return HttpResponse(f"Error sending email: {e}")

"""
This is the development settings module of the Django application.

The module imports base settings from `base.py` and uses environment variables for configuration.
- SENTRY_DSN: environment variable is used to provide the DSN for the Sentry service.

If the `SENTRY_DSN` is present, the Sentry SDK is initialized with the following settings:
- `dsn` is set to `SENTRY_DSN`.
- The `traces_sample_rate` is set to 0.01 to capture 1% of transactions for performance monitoring.
- The `profiles_sample_rate` is set to 0.01 to profile 1% of sampled transactions.
- `send_default_pii` is set to True to enable sending PII data to Sentry.
- `auto_session_tracking` is set to True to automatically start and end sessions.

The SDK is also instructed to ignore log messages from `"django.security.DisallowedHost"`.

- EMAIL_BACKEND: default sender for anymail
- DEBUG_SQL: sql profiler setting: {0: 'disabled', 1: 'enabled'}

Note: The actual values used might vary and should be retrieved from environment variables or a secure configuration mechanism.
"""

from .base import *

# Sentry settings
SENTRY_DSN = os.getenv('SENTRY_DSN', None)

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.logging import ignore_logger

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 0.01 to capture 1%
        # of transactions for performance monitoring.
        traces_sample_rate=0.01,
        # Set profiles_sample_rate to 0.01 to profile 1%
        # of sampled transactions.
        profiles_sample_rate=0.01,
        send_default_pii=True,
        auto_session_tracking=True
    )
    ignore_logger('django.security.DisallowedHost')


# settings to choose default email sender for anymail, choose one of the below or set up your in base.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # free to use, but usually counts as a spam
# EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
# EMAIL_BACKEND = 'anymail.backends.amazon_ses.EmailBackend'
# EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

# sql profiler setting: {0: 'disabled', 1: 'enabled'}
DEBUG_SQL = bool(int(os.environ.get('DEBUG_SQL', 0)))

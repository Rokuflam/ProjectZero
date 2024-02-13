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
    ignore_logger("django.security.DisallowedHost")

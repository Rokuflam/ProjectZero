"""
Here is the place for all custom DB functions
"""
from django.db import models


# pylint: disable=abstract-method
class ConcatOp(models.Func):
    """Custom Concat for Postgres, because it says Concat not immutable"""
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"

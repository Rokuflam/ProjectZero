"""
This module contains custom database functions to be used in the Django application.

The module contains a class `ConcatOp`, a custom class for Concat operation specific to Postgres database.
The Postgres Concat operation is considered not immutable,
 hence it's defined here as a custom database function in Django's ORM.

Warning: This module disables the abstract-method check from pylint for the `ConcatOp` class
as it is a subclass of Django's `models.Func` which is an abstract base class but does not define all
its abstract methods.

Classes:
    ConcatOp: A custom Django database function for a Postgres-specific Concat operation.
"""
from django.db import models


# pylint: disable=abstract-method
class ConcatOp(models.Func):
    """
    A custom Django database function for a Postgres-specific Concat operation.

    The operation is defined using the Django's `models.Func` base class.
    The `arg_joiner` is set to ' || ', which is the SQL standard for Concat operation.
    The `function` is set to None to use basic SQL template.
    The `output_field` is defined as `models.TextField()`, meaning the operation returns a text field.

    The `template` attribute is set to "%(expressions)s" to specify how the SQL string should
    be constructed from the list of expressions.
    """
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"

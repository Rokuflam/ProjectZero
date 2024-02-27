"""
Django management command to wait for the database to be available.

This command routinely checks for the availability of the database. If the database is not available,
the command pauses for 1 second before checking again.
"""

import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """Django command to pause execution until the database is available."""

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        """
        Entry point for the command.

        This method repeatedly tries to establish a connection with the default database.
        If a connection attempt fails, the command waits for 1 second before trying again.
        This process is repeated until a connection with the database is successfully established.
        """
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))

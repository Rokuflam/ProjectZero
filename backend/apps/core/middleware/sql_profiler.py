"""
This module defines a middleware for Django applications that enables SQL profiling.
It is designed to help developers understand and optimize the database interactions of their application
by logging the total number of SQL queries executed for each request and the time taken for each query.

Usage requires setting `DEBUG_SQL` in the Django project's settings.py file. When `DEBUG_SQL` is True,
the middleware logs detailed information about each SQL query executed during the request lifecycle.
This includes the total number of queries and the cumulative time spent on all database interactions.

Intended for development environments, it aids in identifying inefficient database queries and potential
performance bottlenecks.
"""
import time
from django.conf import settings
from django.db import connection


class SQLProfilerMiddleware:
    """
   Middleware for enabling SQL profiling in Django applications.

   Logs the total number of SQL queries executed during the processing of a request
    and the time taken for each, facilitating performance analysis and optimization of database interactions.

   Attributes:
       get_response (callable): A callable that takes a request and returns a response. It is part of the
       middleware chain to process the request or response.

   Methods:
       __init__(self, get_response): Initializes the SQLProfilerMiddleware with the next middleware or view.
       __call__(self, request): Processes the incoming request, enabling SQL profiling if DEBUG_SQL is True.
   """
    def __init__(self, get_response):
        """
        Initialize the SQLProfilerMiddleware instance.

        Args:
            get_response (callable): The next middleware or view in the chain to process the request.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request, logging SQL queries and their execution times if DEBUG_SQL setting is True.

        Checks the `DEBUG_SQL` setting from the Django settings. If it is True,
         logs the details of SQL queries executed during the request's lifecycle,
         including the number of queries and the total time spent on
        database interactions.

        Args:
            request (HttpRequest): The Django HttpRequest object for the current request.

        Returns:
            HttpResponse: The response object returned by the next middleware or view in the chain.
        """
        # Check if SQL profiling is enabled based on DEBUG_SQL setting
        sql_profiling_enabled = settings.DEBUG_SQL
        if sql_profiling_enabled is True:
            # Start timing and tracking queries
            start_time = time.time()
            connection.queries_log.clear()

        response = self.get_response(request)

        if sql_profiling_enabled is True:
            # Calculate total time
            total_time = time.time() - start_time
            total_queries = len(connection.queries)

            # Log the total time and individual query info
            print(f"Total DB Queries: {total_queries}, Total Time Spent: {total_time} seconds")
            for query in connection.queries:
                print(f"Query: {query['sql']}, Time: {query['time']}")

        return response

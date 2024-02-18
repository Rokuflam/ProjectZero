"""
This module defines URL routes for the Django application.

The URL routes are defined with the Django's `path()` function and they are
gathered in the `urlpatterns` list.

Django uses this list to find a match with the current URL and then calls
the associated view function.

The module includes URLs for:
- Django admin (`admin/`)
- User API routes (`api/user/`). The actual routes are defined in 'apps.user.urls' module.

In debug mode (when `settings.DEBUG` is `True`), the module also serves static and media files.

If `settings.SHOW_DOCS` is `True`, this module also adds routes for serving API schema (`api/schema/`)
and API docs (`api/docs/`).

API schema and documentation are served using Django REST framework Spectacular views.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('apps.user.urls')),
    path('api/accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    # enable media on localhost
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

if settings.SHOW_DOCS:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
    )
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
        path(
            'api/docs/',
            SpectacularSwaggerView.as_view(url_name='api-schema'),
            name='api-docs'
        )
     ]

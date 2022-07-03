"""
ASGI config for my_blog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application


if os.environ.get('DJANGO_ENV') == 'production':
    # custom prod settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings.prod')
else:
    # custom dev settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings.dev')

application = get_asgi_application()

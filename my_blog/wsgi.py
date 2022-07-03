"""
WSGI config for my_blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('DJANGO_ENV') == 'production':
    # custom prod settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings.prod')
else:
    # custom dev settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings.dev')

application = get_wsgi_application()

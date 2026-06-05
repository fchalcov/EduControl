"""
Punto de entrada WSGI en la raíz de back/.
Usado por: gunicorn wsgi:application
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application  # noqa: E402,F401

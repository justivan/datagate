from .base import *
from .base import env


SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1"])

ADMIN_URL = env("DJANGO_ADMIN_URL")

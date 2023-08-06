from .base import *
from .base import env


SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-+cwck##kn$i()zxlqlg16l)evacw+0j-e==_%jc=85o))lyz5j",
)

DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

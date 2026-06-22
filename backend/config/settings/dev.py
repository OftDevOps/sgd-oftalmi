from .base import *  # noqa: F403


DEBUG = config("DEBUG", default=True, cast=bool)  # noqa: F405

ALLOWED_HOSTS = config(  # noqa: F405
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1,0.0.0.0",
    cast=Csv(),  # noqa: F405
)

EMAIL_BACKEND = config(  # noqa: F405
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

INTERNAL_IPS = ["127.0.0.1"]

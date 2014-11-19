from distutils.core import Command

import django
from django.conf import settings
from django.core.management import call_command


class TestCommand(Command):
    description = "Launch all tests under django_payzen app"
    user_options = [
        ("site=", None, "Payzen site id (VADS_SITE_ID)"),
        ("certificate=", None, "Payzen certificate (VADS_CERTIFICATE)"),
    ]

    def initialize_options(self):
        self.site = None
        self.certificate = None

    def finalize_options(self):
        if self.site is None:
            raise Exception("\'site\' option is not provided.\n"
                            "Please call \'python setup.py test\' with"
                            " --site option")
        if self.certificate is None:
            raise Exception("\'certificate\' option is not provided.\n"
                            "Please call \'python setup.py test\' with"
                            " --certificate option")

    def configure_settings(self):
        settings.configure(
            DATABASES={
                "default": {
                    "NAME": ":memory:",
                    "ENGINE": "django.db.backends.sqlite3"
                }
            },
            INSTALLED_APPS=(
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django_payzen",
            ),
            MIDDLEWARE_CLASSES = (
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.middleware.csrf.CsrfViewMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
            ),
            VADS_SITE_ID = self.site,
            VADS_CERTIFICATE = self.certificate,
            VADS_CURRENCY = "978",
            VADS_ACTION_MODE = "INTERACTIVE",
            VADS_CTX_MODE = "TEST",
            LOGGING = {
                "version": 1,
                "disable_existing_loggers": True,
                "handlers": {
                    "console": {
                        "level": "INFO",
                        "class": "logging.StreamHandler",
                    },
                },
                "loggers": {
                    "django_payzen": {
                        "handler": ["console"],
                        "propagate": True,
                        "level": "INFO"
                    }
                },
            },
        )

    def run(self):
        self.configure_settings()
        django.setup()
        call_command("test", "django_payzen", liveserver="0.0.0.0:8000")

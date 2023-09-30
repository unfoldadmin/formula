from os import environ, path
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

######################################################################
# General
######################################################################
BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = environ.get("SECRET_KEY", get_random_secret_key())

DEBUG = environ.get("DEBUG", False)

ROOT_URLCONF = "formula.urls"

WSGI_APPLICATION = "formula.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

######################################################################
# Domains
######################################################################
ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "localhost").split(",")

CSRF_TRUSTED_ORIGINS = environ.get(
    "CSRF_TRUSTED_ORIGINS", "http://localhost:8000"
).split(",")

######################################################################
# Apps
######################################################################
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "import_export",
    "django_celery_beat",
    "djmoney",
    "formula",
]

######################################################################
# Middleware
######################################################################
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "formula.middleware.ReadonlyExceptionHandlerMiddleware",
]

######################################################################
# Sessions
######################################################################
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

######################################################################
# Templates
######################################################################
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            path.normpath(path.join(BASE_DIR, "formula/templates")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

######################################################################
# Databases
######################################################################
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ROOT_DIR / "database.sqlite",
    },
}

######################################################################
# Authentication
######################################################################
AUTH_USER_MODEL = "formula.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = "admin:login"

LOGIN_REDIRECT_URL = reverse_lazy("admin:index")

######################################################################
# Localization
######################################################################
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Bratislava"

USE_I18N = True

USE_TZ = True

######################################################################
# Static
######################################################################
STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "formula" / "static"]

STATIC_ROOT = BASE_DIR / "static"

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

######################################################################
# Unfold
######################################################################
UNFOLD = {
    "SITE_HEADER": _("Formula Admin"),
    "SITE_TITLE": _("Formula Admin"),
    "SITE_SYMBOL": "settings",
    "LOGIN": {
        "image": lambda r: static("images/login-bg.jpg"),
    },
    "STYLES": [
        lambda request: static("css/styles.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/chart.min.js"),
    ],
    "TABS": [
        {
            "models": ["formula.driver", "formula.constructor"],
            "items": [
                {
                    "title": _("Drivers"),
                    "icon": "sports_motorsports",
                    "link": reverse_lazy("admin:formula_driver_changelist"),
                },
                {
                    "title": _("Constructors"),
                    "icon": "precision_manufacturing",
                    "link": reverse_lazy("admin:formula_constructor_changelist"),
                },
            ],
        },
        {
            "models": [
                "django_celery_beat.clockedschedule",
                "django_celery_beat.crontabschedule",
                "django_celery_beat.intervalschedule",
                "django_celery_beat.periodictask",
                "django_celery_beat.solarschedule",
            ],
            "items": [
                {
                    "title": _("Clocked"),
                    "icon": "hourglass_bottom",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_clockedschedule_changelist"
                    ),
                },
                {
                    "title": _("Crontabs"),
                    "icon": "update",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_crontabschedule_changelist"
                    ),
                },
                {
                    "title": _("Intervals"),
                    "icon": "arrow_range",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_intervalschedule_changelist"
                    ),
                },
                {
                    "title": _("Periodic tasks"),
                    "icon": "task",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_periodictask_changelist"
                    ),
                },
                {
                    "title": _("Solar events"),
                    "icon": "event",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_solarschedule_changelist"
                    ),
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Drivers"),
                        "icon": "sports_motorsports",
                        "link": reverse_lazy("admin:formula_driver_changelist"),
                    },
                    {
                        "title": _("Circuits"),
                        "icon": "circle",
                        "link": reverse_lazy("admin:formula_circuit_changelist"),
                    },
                    {
                        "title": _("Races"),
                        "icon": "stadium",
                        "link": reverse_lazy("admin:formula_race_changelist"),
                        "badge": "formula.utils.badge_dynamic_value",
                    },
                    {
                        "title": _("Standings"),
                        "icon": "grade",
                        "link": reverse_lazy("admin:formula_standing_changelist"),
                    },
                ],
            },
            {
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:formula_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Tasks"),
                        "icon": "task_alt",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_clockedschedule_changelist"
                        ),
                    },
                ],
            },
        ],
    },
}

######################################################################
# Money
######################################################################
CURRENCIES = ("USD", "EUR")

######################################################################
# App
######################################################################
LOGIN_USERNAME = environ.get("LOGIN_USERNAME")

LOGIN_PASSWORD = environ.get("LOGIN_PASSWORD")

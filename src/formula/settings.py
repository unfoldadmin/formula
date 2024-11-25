from os import environ, path
from pathlib import Path

import sentry_sdk
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
    "modeltranslation",
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "import_export",
    "guardian",
    "simple_history",
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
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
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
                "formula.context_processors.variables",
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

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

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
LANGUAGE_CODE = "en"

TIME_ZONE = "Europe/Bratislava"

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ("de", _("German")),
    ("en", _("English")),
)

# https://docs.djangoproject.com/en/5.1/ref/settings/#date-input-formats
DATE_INPUT_FORMATS = [
    "%d.%m.%Y",  # Custom input
    "%Y-%m-%d",  # '2006-10-25'
    "%m/%d/%Y",  # '10/25/2006'
    "%m/%d/%y",  # '10/25/06'
    "%b %d %Y",  # 'Oct 25 2006'
    "%b %d, %Y",  # 'Oct 25, 2006'
    "%d %b %Y",  # '25 Oct 2006'
    "%d %b, %Y",  # '25 Oct, 2006'
    "%B %d %Y",  # 'October 25 2006'
    "%B %d, %Y",  # 'October 25, 2006'
    "%d %B %Y",  # '25 October 2006'
    "%d %B, %Y",  # '25 October, 2006'
]

# https://docs.djangoproject.com/en/5.1/ref/settings/#datetime-input-formats
DATETIME_INPUT_FORMATS = [
    "%d.%m.%Y %H:%M:%S",  # Custom input
    "%Y-%m-%d %H:%M:%S",  # '2006-10-25 14:30:59'
    "%Y-%m-%d %H:%M:%S.%f",  # '2006-10-25 14:30:59.000200'
    "%Y-%m-%d %H:%M",  # '2006-10-25 14:30'
    "%m/%d/%Y %H:%M:%S",  # '10/25/2006 14:30:59'
    "%m/%d/%Y %H:%M:%S.%f",  # '10/25/2006 14:30:59.000200'
    "%m/%d/%Y %H:%M",  # '10/25/2006 14:30'
    "%m/%d/%y %H:%M:%S",  # '10/25/06 14:30:59'
    "%m/%d/%y %H:%M:%S.%f",  # '10/25/06 14:30:59.000200'
    "%m/%d/%y %H:%M",  # '10/25/06 14:30'
]

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
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

######################################################################
# Unfold
######################################################################
UNFOLD = {
    "SITE_HEADER": _("Formula Admin"),
    "SITE_TITLE": _("Formula Admin"),
    "SITE_SYMBOL": "settings",
    # "SHOW_HISTORY": True,
    "SHOW_LANGUAGES": True,
    "ENVIRONMENT": "formula.utils.environment_callback",
    "DASHBOARD_CALLBACK": "formula.views.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("images/login-bg.jpg"),
    },
    "STYLES": [
        lambda request: static("css/styles.css"),
    ],
    "SCRIPTS": [
        # lambda request: static("js/chart.min.js"),
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
                    "title": _("Active drivers"),
                    "icon": "sports_motorsports",
                    "link": lambda request: f"{reverse_lazy(
                        "admin:formula_driver_changelist"
                    )}?status__exact=ACTIVE",
                },
                {
                    "title": _("Inactive drivers"),
                    "icon": "sports_motorsports",
                    "link": lambda request: f"{reverse_lazy(
                        "admin:formula_driver_changelist"
                    )}?status__exact=INACTIVE",
                },
                {
                    "title": _("Constructors"),
                    "icon": "precision_manufacturing",
                    "link": reverse_lazy("admin:formula_constructor_changelist"),
                },
                {
                    "title": _("Custom page"),
                    "icon": "grade",
                    "link": reverse_lazy("admin:custom_view"),
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
                        # "link": lambda request: reverse_lazy(
                        #     "admin:formula_driver_changelist"
                        # ),
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
                        "badge": "formula.utils.badge_callback",
                    },
                    {
                        "title": _("Standings"),
                        "icon": "grade",
                        "link": reverse_lazy("admin:formula_standing_changelist"),
                        "permission": "formula.utils.permission_callback",
                        # "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Users & Groups"),
                "collapsible": True,
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
                ],
            },
            {
                "title": _("Celery Tasks"),
                "collapsible": True,
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

############################################################################
# Debug toolbar
############################################################################
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}

######################################################################
# Plausible
######################################################################
PLAUSIBLE_DOMAIN = environ.get("PLAUSIBLE_DOMAIN")

######################################################################
# Sentry
######################################################################
SENTRY_DSN = environ.get("SENTRY_DSN")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        enable_tracing=False,
    )

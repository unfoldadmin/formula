import random

from django.conf import settings
from django.utils.translation import gettext_lazy as _


def environment_callback(request):
    if settings.DEBUG:
        return [_("Development"), "info"]

    return [_("Production"), "warning"]


def badge_callback(request):
    return f"+{random.randint(1, 99)}"


def permission_callback(request):
    return True

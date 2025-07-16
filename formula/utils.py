import random

from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def environment_callback(request):
    if settings.DEBUG:
        return [_("Development"), "primary"]

    return [_("Production"), "primary"]


def badge_callback(request):
    return f"{random.randint(1, 9)}"


def permission_callback(request):
    return True


def driver_link_callback(request):
    return (
        lambda request: str(reverse_lazy("admin:formula_driver_changelist"))
        in request.path
        or request.path == reverse_lazy("admin:formula_driverwithfilters_changelist")
        or request.path == reverse_lazy("admin:crispy_form")
        or request.path == reverse_lazy("admin:crispy_formset")
    )


def driver_list_link_callback(request):
    if request.path == reverse_lazy("admin:formula_driver_changelist"):
        return True

    if str(reverse_lazy("admin:formula_driver_changelist")) in request.path:
        return True

    if str(reverse_lazy("admin:formula_driverwithfilters_changelist")) in request.path:
        return True

    return False


def driver_list_sublink_callback(request):
    if str(reverse_lazy("admin:crispy_form")) in request.path:
        return False

    if str(reverse_lazy("admin:crispy_formset")) in request.path:
        return False

    if request.path == reverse_lazy("admin:formula_driver_changelist"):
        return True

    if str(reverse_lazy("admin:formula_driver_changelist")) in request.path:
        return True

    return False

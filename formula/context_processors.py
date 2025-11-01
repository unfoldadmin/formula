from os import environ

from django.conf import settings


def variables(request):
    return {
        "plausible_domain": settings.PLAUSIBLE_DOMAIN,
        "studio_installed": environ.get("UNFOLD_STUDIO") == "1",
    }

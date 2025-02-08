from django.conf import settings


def variables(request):
    return {
        "plausible_domain": settings.PLAUSIBLE_DOMAIN
    }

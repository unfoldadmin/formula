from django.views.generic import RedirectView


class HomeView(RedirectView):
    pattern_name = "admin:index"

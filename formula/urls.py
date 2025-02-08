from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import include, path

from formula.sites import formula_admin_site
from formula.views import HomeView

urlpatterns = (
    [
        path("", HomeView.as_view(), name="home"),
        path("i18n/", include("django.conf.urls.i18n")),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    + i18n_patterns(
        path("admin/", formula_admin_site.urls),
    )
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

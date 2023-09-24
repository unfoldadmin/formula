from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from formula.sites import formula_admin_site
from formula.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", formula_admin_site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

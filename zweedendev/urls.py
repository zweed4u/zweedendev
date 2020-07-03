from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

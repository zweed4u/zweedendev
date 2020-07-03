from zweedendev import views
from django.urls import path


urlpatterns = [
    # api/v1/info
    path("info", views.list_info, name="list_info"),
]

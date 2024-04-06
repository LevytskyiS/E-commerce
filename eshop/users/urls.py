from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path(
        "profile/<int:pk>/",
        views.UserDetailView.as_view(),
        name="user_detail",
    ),
]

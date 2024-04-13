from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("profile/<str:username>/", views.ProfileDetailView.as_view(), name="profile"),
    path(
        "update/<int:pk>/",
        views.ProfileUpdateView.as_view(),
        name="update_profile",
    ),
]

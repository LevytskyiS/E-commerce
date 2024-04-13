from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    # Login, registration, logout, password reset
    path("registration/", views.RegisterUser.as_view(), name="registration"),
    path(
        "registration_confirmation/",
        views.registration_confirmation,
        name="registration_confirmation",
    ),
    path("profile/<str:username>/", views.ProfileDetailView.as_view(), name="profile"),
    path(
        "update/<int:pk>/",
        views.ProfileUpdateView.as_view(),
        name="update_profile",
    ),
]

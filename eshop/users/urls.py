from django.urls import path
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

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
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", views.LogOutUser.as_view(), name="logout"),
    path("reset_password/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "reset_password/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset_password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url="/users/reset_password/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # User detail, update
    path("profile/<str:username>/", views.ProfileDetailView.as_view(), name="profile"),
    path(
        "update/<int:pk>/",
        views.ProfileUpdateView.as_view(),
        name="update_profile",
    ),
]

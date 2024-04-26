from django.urls import path

from users.views import (
    RegisterView,
    LoginView,
    LogoutView,
    EmailConfirmView,
    SettingsView,
    StatsView,
    PasswordResetRequestView,
    PasswordResetView,
)

urlpatterns = [
    path(
        'register/',
        RegisterView.as_view(),
        name='register',
    ),
    path(
        'login/',
        LoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout',
    ),
    path(
        'confirm_email/<str:url_hash>/',
        EmailConfirmView.as_view(),
        name='confirm_email',
    ),
    path(
        'settings/',
        SettingsView.as_view(),
        name='settings',
    ),
    path(
        'stats/',
        StatsView.as_view(),
        name='stats',
    ),
    path(
        'password_reset/request/',
        PasswordResetRequestView.as_view(),
        name='password_reset_request',
    ),
    path(
        'password_reset/<str:url_hash>/',
        PasswordResetView.as_view(),
        name='password_reset',
    ),
]


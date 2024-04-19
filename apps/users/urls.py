from django.urls import path
from users.views import (
    RegisterView,
    LoginView,
    LogoutView,
    EmailConfirmView,
    SettingsView,
    stats_view,
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
        'confirm/<str:url_hash>/',
        EmailConfirmView.as_view(),
        name='confirm',
    ),
    path(
        'settings/',
        SettingsView.as_view(),
        name='settings',
    ),
    path(
        'stats/',
        stats_view,
        name='stats',
    ),
]

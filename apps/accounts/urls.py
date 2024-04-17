from django.urls import path
from accounts.views import (
    RegisterView,
    LoginView,
    EmailConfirmView,
    profile_view,
    settings_view,
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
        'confirm/<str:email>/<str:token>/',
        EmailConfirmView.as_view(),
        name='confirm',
    ),
    path(
        'profile/',
        profile_view,
        name='profile',
    ),
    path(
        'settings/',
        settings_view,
        name='settings',
    ),
    path(
        'stats/',
        stats_view,
        name='stats',
    ),
]

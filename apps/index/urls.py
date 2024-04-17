from django.urls import path
from index.views import Index


urlpatterns = [
    path(
        '',
        Index.as_view(),
        name='index',
    ),
]

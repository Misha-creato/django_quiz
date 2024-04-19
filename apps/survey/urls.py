from django.urls import path

from survey.views import SurveyDetail


urlpatterns = [
    path(
        '<int:pk>/',
        SurveyDetail.as_view(),
        name='survey',
    ),
]

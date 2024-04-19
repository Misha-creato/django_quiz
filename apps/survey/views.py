from django.views import View
from django.shortcuts import (
    render,
    get_object_or_404,
)

from survey.models import Survey


class SurveyDetail(View):
    def get(self, request, pk):
        survey = get_object_or_404(
            klass=Survey,
            pk=pk
        )
        context = {
            'survey': survey
        }
        return render(
            request=request,
            template_name='survey.html',
            context=context,
        )

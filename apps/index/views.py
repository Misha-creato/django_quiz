from django.shortcuts import render
from django.views import View
from django.db.models import Q

from survey.models import Survey


class Index(View):
    def get(self, request, *args, **kwargs):
        user = request.user.id
        survey = Survey.objects.first()
        if user:
            survey = Survey.objects.filter(~Q(options__users=user)).first()
        context = {
            'survey': survey
        }
        return render(
            request=request,
            template_name='index.html',
            context=context,
        )

    def post(self, request, *args, **kwargs):
        option = request.POST['option']
        user = request.user
        user.options.add(option)
        survey_stats = Survey.objects.filter(options__id=option).first()
        context = {
            'survey_stats': survey_stats,
        }
        return render(
            request=request,
            template_name='index.html',
            context=context,
        )

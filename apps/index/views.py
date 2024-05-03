from django.shortcuts import (
    render,
    redirect,
)
from django.views import View
from django.db.models import Q
from django.contrib import messages

from survey.models import Survey


class IndexView(View):
    def get(self, request, *args, **kwargs):
        user = request.user.id
        if user:
            survey = Survey.objects.filter(
                ~Q(options__users=user)
            ).prefetch_related('options').first()
        else:
            survey = Survey.objects.first()
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
        messages.success(
            request=request,
            message='Спасибо, Ваш выбор учтён. Вы можете просмотреть статистику в профиле.',
        )
        return redirect('index')

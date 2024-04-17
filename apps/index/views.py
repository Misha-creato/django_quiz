from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='index.html')

    def post(self, request, *args, **kwargs):
        context = {
            'response': 'Спасибо, Ваш выбор учтён, Вы можете просмотреть статистику по ссылке'
        }
        return render(request=request, template_name='index.html', context=context)

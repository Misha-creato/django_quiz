from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()


class Survey(models.Model):
    question = models.CharField(
        max_length=256,
        verbose_name='Вопрос',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    @property
    def count_voted(self):
        return self.options.aggregate(Count('users'))['users__count']

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        db_table = 'survey'


class Option(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    order = models.IntegerField(
        default=1,
        verbose_name='Порядковый номер',
    )
    survey = models.ForeignKey(
        to=Survey,
        on_delete=models.CASCADE,
        related_name='options',
    )
    users = models.ManyToManyField(
        to=User,
        blank=True,
        related_name='options',
    )

    @property
    def count_voted(self):
        return self.users.count()

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        db_table = 'option'

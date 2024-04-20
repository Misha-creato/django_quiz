from django.contrib import admin

from survey.models import (
    Survey,
    Option,
)


class OptionInline(admin.StackedInline):
    model = Option
    extra = 1
    fields = (
        'order',
        'title',
    )


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'description',
    )
    inlines = (
        OptionInline,
    )

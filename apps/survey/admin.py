from django.contrib import admin
from survey.models import (
    Survey,
    Option,
)


class OptionInline(admin.TabularInline):
    model = Option
    extra = 3
    fields = (
        'title',
        'order',
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

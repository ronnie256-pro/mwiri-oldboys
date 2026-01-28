from django.contrib import admin
from .models import TeaserQuestion, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

@admin.register(TeaserQuestion)
class TeaserQuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

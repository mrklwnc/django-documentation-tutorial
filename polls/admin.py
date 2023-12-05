from django.contrib import admin

from .models import Choice, Question

# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'choice_text', 'votes')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)

from django.contrib import admin

from .models import Choice, Question

# Register your models here.


class ChoiceInline(admin.TabularInline):  # admin.StackedInline or TabularInline
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # Customize Admin Form (Question Model)
    # See https://docs.djangoproject.com/en/4.2/intro/tutorial07/

    # fields = ["pub_date", "question_text"]

    # Using fieldsets (The first element of each tuple in fieldsets is the title of the fieldset)
    fieldsets = [
        ("QUESTION DETAILS", {"fields": ["question_text", "pub_date"]}),
    ]

    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date',
                    'was_published_recently', 'hasChoices')

    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    list_per_page = 10


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'choice_text', 'votes')


# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice, ChoiceAdmin)

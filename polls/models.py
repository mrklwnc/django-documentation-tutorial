import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?"
    )
    def was_published_recently(self):
        # This was a bug intended to be fixed in Django Tutorial part 5
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

        # This was the fixed version
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    # was_published_recently.short_description = "Was Published recently"

    def hasChoices(self):
        return self.choices.exists()
    hasChoices.short_description = "Has Choices"


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def question_id(self):
        return self.question.id
    question_id.short_description = "QID"

    def __str__(self):
        return self.choice_text

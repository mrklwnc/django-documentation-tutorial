from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from django.db.models import Count

from .models import Choice, Question

# Create your views here.


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {
#         "latest_question_list": latest_question_list
#     }
#     return render(request, "index.html", context)


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "detail.html", {"question": question})

class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions with available choices
        """
        return Question.objects.annotate(num_choices=Count('choices')).filter(num_choices__gt=0).order_by("-pub_date")[:5]

# NOTE: Without using Generic Views
# def detail(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     return render(request, "detail.html", {"question": question})


# ? Using Generic Views
class DetailView(generic.DetailView):
    template_name = "detail.html"
    context_object_name = "question"

    def get_queryset(self):
        return Question.objects.filter(pk=self.kwargs.get("pk"))


def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)

    try:
        selected_choice = question.choices.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "detail.html", {"question": question, "error_message": "You didn't select a choice."})
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# def results(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     return render(request, "results.html", {"question": question})

class ResultsView(generic.DetailView):
    template_name = "results.html"
    context_object_name = "question"

    def get_queryset(self):
        return Question.objects.filter(pk=self.kwargs.get("pk"))

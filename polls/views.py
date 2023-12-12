from json import loads, dump
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from django.db.models import Count
from django.core.serializers import serialize

from django.contrib.auth.models import User
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
        return Question.objects.annotate(num_choices=Count('choices')).filter(pub_date__lte=timezone.now(), num_choices__gt=0).order_by("-pub_date")[:5]

# NOTE: Without using Generic Views
# def detail(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     return render(request, "detail.html", {"question": question})


# ? Using Generic Views
class DetailView(generic.DetailView):
    template_name = "detail.html"
    context_object_name = "question"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now(), pk=self.kwargs.get("pk"))


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


# serializer flatten
def flatten_fields(inst: dict, excluded=[]) -> dict:
    inst = {**inst["fields"], **inst}
    trimmed_inst = {
        key: inst[key] for key in inst.keys() if key not in excluded
    }
    del trimmed_inst["fields"]

    return trimmed_inst


# Serialize a single model instance
def single(request, pk):
    item = User.objects.get(pk=pk)
    # dumps item as JSON array with 1 value
    serialized_data = serialize("json", [item])
    # load as Python Dict and get the only value
    dumped_item = loads(serialized_data)[0]
    flattened_item = flatten_fields(
        dumped_item, ["password", "is_superuser", "is_staff"])

    return JsonResponse(flattened_item)


# Serialize a list of model instances
def list(request):
    item = User.objects.all()
    # dumps item as JSON array with 1 value
    serialized_data = serialize("json", item)
    # load as Python Dict and get the only value
    dumped_item = loads(serialized_data)

    flattened_fields = []

    for field in dumped_item:
        flattened_item = flatten_fields(
            field, ["password", "is_superuser", "is_staff"])
        flattened_fields.append(flattened_item)

    return JsonResponse(flattened_fields, safe=False)

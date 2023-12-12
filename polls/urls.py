from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:pk>/results/", views.results, name="results"),
    path("<int:pk>/vote/", views.vote, name="vote"),

    # Paths used for serializer examples.
    path("sample/<int:pk>/", views.single, name="single"),
    path("sample-list/", views.list, name="list"),
]

"""
Using Generic Views - Django Tutorial part 4

https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-display/
"""

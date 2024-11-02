from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contribute", views.contribute, name="contribute"),
    path("data", views.data, name="data"),
    path("submit", views.submit, name="submit")
]

from django.urls import path
from main import views

urlpatterns = [
    path("", views.home, name="home"),
    path("watch/<id>", views.watch, name="watch"),
    path("channle/<id>", views.channle, name="channle"),
]
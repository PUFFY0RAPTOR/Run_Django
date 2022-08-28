from django.urls import path

from . import views

app_name="run"

urlpatterns = [
    path('', views.index, name='index'),
]
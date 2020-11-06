from django.urls import include, path
from mainapp import views

urlpatterns = [
    path('', views.index, name='index'),
]


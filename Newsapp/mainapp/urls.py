from django.urls import include, path
from mainapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('makeAccount', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('signin', views.signin, name='signin')
]


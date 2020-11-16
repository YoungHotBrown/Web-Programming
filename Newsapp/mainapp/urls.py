from django.urls import include, path
from mainapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'), # Loads the signup page with the form
    path('signup', views.signup, name='signup'), # View for processing signup
    path('login', views.login, name='login'), # Loads the login page with the form
    path('signin', views.signin, name='signin'), # Processes the login
    path('displayArticles', views.displayArticles, name='articles'),
    path('logout', views.logout, name='logout'),
]


from django.shortcuts import render

# Create your views here.

appname = 'News' #Application name

#index view displays the home page of the application
def index(request):
    context = {'appname': appname}
    return render(request, 'mainapp/index.html', context)

def register(request):
    context = {'appname': appname}
    return render(request, 'mainapp/register.html', context)



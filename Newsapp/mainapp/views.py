from django.shortcuts import render
from django.http import HttpResponse, Http404
#for testing remove later
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

appname = 'News' #Application name

#index view displays the home page of the application
def index(request):
    context = {'appname': appname}
    return render(request, 'mainapp/index.html', context)

def register(request):
    context = {'appname': appname}
    return render(request, 'mainapp/register.html', context)

@csrf_exempt # just for testing purposes cant pass csrf using insomnia
def makeAccount(request):
    email = request.POST["Email"]
    name = request.POST["Flname"]
    dob = request.POST["DOB"]
    password = request.POST["Password"]

    if email and name and dob and password:
        HttpResponse("bad man")
    else:
        raise Http404("Wasteman")
#not complete will finish this

from django.shortcuts import render
from django.http import HttpResponse, Http404
#for testing remove later
from django.views.decorators.csrf import csrf_exempt

from .models import Member, Article

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
    #taking all form values out of the POST Dictionairy
    #USE INSOMNIA TO TEST HAVENT ACTUALLY SET THE FROM ACTION TO THIS YET

    if 'Username' in request.POST and 'Email' in request.POST and 'Flname' in request.POST and 'DOB' in request.POST and 'Password' in request.POST:
        username = request.POST["Username"]
        email = request.POST["Email"]
        name = request.POST["Flname"]
        dob = request.POST["DOB"]
        password = request.POST["Password"]

        #return HttpResponse("lol")
        #Save the member
        member = Member(username = username, email = email, first_name = name, date_of_birth = dob)
        member.set_password(password) #Automatically Hashes the password

        try: member.save()
        except IntegrityError: raise Http404('Error User could not be registered') # user is registered but integrity error not working
        # Potentially add feature to email new member 
        context = {'appname': appname, 'userName': name}
        return render(request, 'mainapp/userRegistered.html', context)
    else:
        raise Http404("RAHH U MAD")

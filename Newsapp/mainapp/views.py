from django.shortcuts import render
from django.http import HttpResponse, Http404
#for testing remove later
from django.views.decorators.csrf import csrf_exempt
import datetime
from .models import Member, Article

# Create your views here.

appname = 'NewsHub' #Application name

#index view displays the home page of the application
def index(request):
    context = {'appname': appname}
    return render(request, 'mainapp/index.html', context)

def register(request):
    context = {'appname': appname}
    return render(request, 'mainapp/register.html', context)

def login(request):
    context = {'appname': appname}
    return render(request, 'mainapp/login.html', context)

@csrf_exempt # just for testing purposes cant pass csrf using insomnia
def signup(request):
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

@csrf_exempt
def signin(request):
    if 'Username' in request.POST and 'Password' in request.POST:
        username = request.POST['Username']
        password = request.POST['Password']

        try: member = Member.objects.get(username = username) # Checking the given username exists
        except Member.DoesNotExist : raise Http404("Member does not exist")

        if member.check_password(password): #Compare the password given to the hashed password in the DB
            #Set session variables for the user logged in
            request.session['Username'] = username
            request.session['Password'] = password 

            #Set cookie
            timeNow = datetime.datetime.utcnow()
            age = 365 * 24 * 60 * 60
            delta = timeNow + datetime.timedelta(seconds=age)
            format = "%a, %d-%b-%Y %H:%M:%S GMT"
            expiration = datetime.datetime.strftime(delta, format)
            #Set login in context to be passed to template
            context = {'appname': appname, 'logIn': True, 'name': username}
            #create variable res to store render so cookie can be set to it
            res = render(request, 'mainapp/login.html', context) # change from login
            res.set_cookie('lastLogin', timeNow, expires=expiration)
            return res
        else:
            raise Http404('Incorrect Password')


        return HttpResponse("Nice it works")
    else:
        context = {'appname': appname, 'error': 'Please Enter the correct login in details'}
        return render(request, 'mainapp/login.html', context)

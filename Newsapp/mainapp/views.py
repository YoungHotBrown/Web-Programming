from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
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

# Register View displays the register page
def register(request):
    context = {'appname': appname}
    return render(request, 'mainapp/register.html', context)

# Login views used to display the login page
def login(request):
    context = {'appname': appname}
    return render(request, 'mainapp/login.html', context)

# Signup view used to process form data and sign users up
def signup(request):

    #Check to see if the request objects POST dictionairy contains all the fields
    if 'Username' in request.POST and 'Email' in request.POST and 'Flname' in request.POST and 'DOB' in request.POST and 'Password' in request.POST:
        #taking all form values out of the POST Dictionairy
        username = request.POST["Username"]
        email = request.POST["Email"]
        name = request.POST["Flname"]
        dob = request.POST["DOB"]
        password = request.POST["Password"]

        #Save the member
        member = Member(username = username, email = email, first_name = name, date_of_birth = dob)
        member.set_password(password) #Automatically Hashes the password

        try: member.save()
        except IntegrityError: raise Http404('This username or password is already taken')

        # Email Feature
        subject = "Thank You From NEWSHUB"
        message = "Thank You for Registering with NEWSHUB " + name
        email_from = settings.EMAIL_HOST_USER
        recipient = [email]
        send_mail( subject, message, email_from, recipient )

        context = {'appname': appname, 'userName': name}
        return render(request, 'mainapp/userRegistered.html', context)
    else:
        raise Http404("The Fields required to register an employee are not present")

# signin view used to process form data and sign user in
def signin(request):
    # Checks fields are present in request object
    if 'Username' in request.POST and 'Password' in request.POST:
        # Extract fields from request and store in varibales
        username = request.POST['Username']
        password = request.POST['Password']

         # Checking the given username exists
        try: member = Member.objects.get(username = username)
        except Member.DoesNotExist :
            #raise Http404("Member does not exist") -- Could do this or re render template with error like below
            context = {'appname': appname, 'error': 'Please Enter the Correct LoginIn Details'}
            return render(request, 'mainapp/login.html', context)

         #Compare the password given to the hashed password in the DB
        if member.check_password(password):
            #Set session variables for the user logged in
            request.session['Username'] = username


            #MAY NOT NEED TO STORE PASSWORD IN SESSION VARIABLE, LEAVE COMMENTED FOR NOW
            #request.session['Password'] = password 
            

            #May NOT NEED COOKIES LEAVE COMMENTED FOR NOW


            #Set cookie
            # timeNow = datetime.datetime.utcnow()
            # age = 365 * 24 * 60 * 60 #time in seconds the cookie will last
            # delta = timeNow + datetime.timedelta(seconds=age)
            # format = "%a, %d-%b-%Y %H:%M:%S GMT"
            # expiration = datetime.datetime.strftime(delta, format)
            # #Set login in context to be passed to template
            # context = {'appname': appname, 'logIn': True, 'name': username}
            # #create variable res to store render so cookie can be set to it
            # res = render(request, 'mainapp/Logged_in_home.html', context) # change from login
            # res.set_cookie('lastLogin', timeNow, expires=expiration)
            # return res

            context = {'logIn': True, 'name': username, 'appname': appname}
            return render(request, 'mainapp/Logged_in_home.html', context)
        else:
            #raise Http404('Incorrect Password')
            context = {'appname': appname, 'error': 'Please Enter the Correct Login In Details'}
            return render(request, 'mainapp/login.html', context)

    else:
        raise Http404("NO USERNAME AND PASSWORD IN REQUEST OBJECT")
        #context = {'appname': appname, 'error': 'Please Enter the correct login in details'}
        #return render(request, 'mainapp/login.html', context)

# Logout and flush session variables
def logout(request):
    request.session.flush()
    context = {'appname': appname}
    return render(request, 'mainapp/Logged_out.html', context)


def displayArticles(request):
    if 'Username' in request.session:
        articles =  Article.objects.all().values('article_name', 'article_author', 'article_date', 'article_tag', 'article_contents')
        context = {'appname': appname, 'logIn': True, 'articles': articles}
        return render(request, 'mainapp/Articles.html', context)
    else:
        raise Http404("This page can only be accessed by logged in users")

#Todo
#Create descorator for user check
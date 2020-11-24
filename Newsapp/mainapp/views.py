from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db import IntegrityError

#Imported for email
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

#Decorator to check users are logged in before loading the requested page
def verify_login(view):
    def usercheck(request):
        if 'Username' in request.session:
            user = request.session['Username']
            try: member = Member.objects.get(username=user)
            except Member.DoesNotExist : raise Http404("User does not exist")
            return view(request, member)
        else:
            context = {'appname': appname}
            return render(request, 'mainapp/Not-Logged-in.html', context)
    return usercheck

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
        # Extract fields from request.POST and store in variables
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
@verify_login
def logout(request, member):
    request.session.flush()
    context = {'appname': appname}
    return render(request, 'mainapp/Logged_out.html', context)

#view used to display the article in a database
@verify_login
def displayArticles(request, member):
    if member.interest_tag == 'None':
        articles =  Article.objects.all().values('article_name', 'article_author', 'article_date', 'article_tag', 'article_contents')
        context = {'appname': appname, 'logIn': True, 'articles': articles}
        return render(request, 'mainapp/Articles.html', context)
    else:
        tag = member.interest_tag
        
        articles =  Article.objects.all().filter(article_tag = tag)
        context = {'appname': appname, 'logIn': True, 'articles': articles}
        return render(request, 'mainapp/Articles.html', context)


#View used to show user detail on the profile
@verify_login
def ProfilePage(request, member):
    context = {'appname': appname, 'logIn': True, 'profile': member}
    return render(request, 'mainapp/Profile.html', context)

#View used to change user profile picture
@verify_login
def ChangeImage(request, member):
    if 'profilepic' in request.POST:
        profilepic = request.POST['profilepic']
        member.profile_picture = profilepic
        member.save()
        context = {'appname': appname, 'logIn': True, 'profile': member}
        return render(request, 'mainapp/Profile.html', context)
    else:
        raise Http404("profilepic does not exist")

@verify_login
def changeInterest_tag(request, member):
    if 'interest_tag' in request.POST:
        interestTag = request.POST['interest_tag']
        member.interest_tag = interestTag
        member.save()
        context = {'appname': appname, 'logIn': True, 'profile': member}
        return render(request, 'mainapp/Profile.html', context)
    else:
        raise Http404("The field interest_tag does not exist")
        


    

#Todo
#Create descorator for user check - Done
#Fix user profile image display + fix error
#change interest tag endpoint - Done
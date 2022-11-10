from django.shortcuts import render, redirect
from basic_app.forms import UserForm, UserProfileInfoForm

# signin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
# if you want a user to be logged in before seeing a view, use login_required
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    '''sign in page'''
    return render(request, 'basic_app/index.html')

def home(request):
    '''home page'''
    return render(request, 'basic_app/home.html')

def register(request):
    '''register page, registered is set to false until form is submitted and verified'''
    registered = False
 
    # if they submit the form w/ POST
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # verify that the forms are valid and save to database
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # save profile pic if user submitted one
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
        
            # registed is set to true, thank you is displayed (see html tag)
            registered = True
            
        else:
            # form has errors
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/register.html',{
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered,
    })

def signin(request):
    # user has filled out and submitted sign in info
    if request.method == 'POST':
        usern = request.POST.get('username')
        # you are using .get('username) on this:
        # <input type="text" NAME="username" placeholder="Username">
        passw = request.POST.get('password')

        # use Djangos built in authentication function
        user = authenticate(username=usern, password=passw)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/basic_app/Home/')

            else:
                return HttpResponse("Account is not active, cannot sign in")
        else:
            # print("Someone tried to login and failed!")
            # print(f"Attempted login : {usern}, {passw}")
            err_message = True
            return render(request, 'basic_app/index.html', {'err_message':err_message})
    else:
        return render(request, 'basic_app/index.html', {})

# make sure someone is logged in to see this view!
# do this with decorator
@login_required
def signout(request):
    '''only if user is signed in, sign them out'''
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def contact(request):
    '''contact page'''
    return render(request, 'basic_app/contact.html')
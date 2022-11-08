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
    return render(request, 'basic_app/index.html')

def home(request):
    return render(request, 'basic_app/home.html')

def register(request):
    registered = False
 
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
        
            registered = True
            
        else:
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
    # user has filled out and submitted login info
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
            print("Someone tried to login and failed!")
            print(f"Attempted login : {usern}, {passw}")
            return HttpResponse('Invalid login credentials provided, please try again')
    else:
        return render(request, 'basic_app/index.html', {})

@login_required
def signout(request):
    # make sure someone is logged in to see this view!
    # do this with decorator
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def contact(request):
    return render(request, 'basic_app/contact.html')
from django.shortcuts import render
from fifth_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'fifth_app/home.html')


@login_required
def special(request):
    return HttpResponse(content="You are logged in")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def register(request):

    registered = False
        # This is the variable passed in the registration.html file to check if user is registered
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
                # if there is profile pic present - it will assign value got in string
                # to profile.profile_pic and then save
                # if nothing present it will not pass anything

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'fifth_app/registration.html',
                        {
                        'user_form':user_form,
                        'profile_form':profile_form,
                        'registered':registered
                        })

def user_login(request):
    if request.method == 'POST':
        urname = request.POST.get('username')
        psword = request.POST.get('password')

        user = authenticate(urname=username,psword=password)

        if user:
            # if user is authenticated
            if user.is_active:
                login(request,user)
                # user is the attribute from line 55 above
                # login is inbuilt django function which was imported to login user
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse(content="Not active")
        else:
            print("Username: {} and password {}".format(username,password))
    else:
        return render(request,'fifth_app/login.html',{})

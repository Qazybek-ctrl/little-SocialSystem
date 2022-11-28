from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.models import User
from .forms import LoginUserForm, RegisterForm

# Create your views here.
def loginPage(request):

    context = {}

    if request.method == 'POST': 
        form = LoginUserForm(request.POST)  
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            user1 = User.objects.filter(username = username)
            form = LoginUserForm(request.POST)
            if len(user1) < 1:
                messages.success(request, ("Username doesn't exist"))
                return render(request, 'Auth/login.html', {'form': form})
            else :
                messages.success(request, ("Password is incorrect..."))
                return render(request, 'Auth/login.html', {'form': form})
    else:
        form = LoginUserForm()           

    context['form'] = form

    return render(request, 'Auth/login.html', context)

def registerPage(request):

    context = {
        'form': RegisterForm
    }

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully :)')
            return redirect('login')
        else:
            form = RegisterForm(request.POST)
            context['form'] = form

    return render(request, 'Auth/register.html', context)

def forgotPassPage(request):
    return render(request, 'Auth/forgotPass.html')

def logOut(request):
    logout(request)
    return redirect('home')
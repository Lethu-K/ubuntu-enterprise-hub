from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, user_type=user_type)
        login(request, user)
        return redirect('/accounts/login/')
    return render(request, 'signup.html')

from django.contrib.auth import authenticate, login as auth_login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/accounts/dashboard/')
        else:
            return render(request, 'login.html', {'error': 'Wrong username or password'})
    return render(request, 'login.html')
from django.contrib.auth.decorators import login_required
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')
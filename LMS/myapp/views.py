from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Employees

# Create your views here.
#def home(request):
 #   return render(request, 'login.html')


def empdashboard(request):
    return render(request, 'employee/dashboard.html')

def logins(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        # Handle invalid login here
        else:
            messages.error(request, "Invalid Credentials. Please check your username and password.")

    return render(request, 'login.html')

def forgotpass(request):
    return render(request, 'forgotpassword.html')

def applyleave(request):
    return render(request, 'applyleave.html')

def leavehistory(request):
    return render(request, 'leavehistory.html')

def profile(request):
    return render(request, 'profile.html')

def emppage(request):
    return render(request, 'emppage.html')

def register(request):
    return render(request, 'register.html')


#admin side views

def dashboard(request):
    return render(request, 'admin/dashboard.html')

def adminleavehistory(request):
    return render(request, 'admin/leavehistory.html')


def adminapplyleave(request):
    return render(request, 'admin/applyleave.html')


def leaveRequest(request):
    return render(request,'admin/leaveRequest.html')


def adminprofile(request):
    return render(request, 'admin/profile.html')






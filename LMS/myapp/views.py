from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Employees, Department, Designation
from django.http import HttpResponse

# Create your views here.
#def home(request):
 #   return render(request, 'login.html')

def dashboard(request):
    return render(request, 'admin/dashboard.html')

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
    if request.method == 'POST':
        empid = request.POST['empid']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        doj = request.POST['doj']
        desig = request.POST['desig']
        dept = request.POST['dept']

        if dept == 'Other':
            other_dept = request.POST['other_dept']
            dept_object, created = Department.objects.get_or_create(dep_name=other_dept)
        else:
            dept_object, created = Department.objects.get_or_create(dep_name=dept)

        desig_object, created = Designation.objects.get_or_create(designation=desig, dep=dept_object)


        new_user = Employees(
            emp_id=empid,
            firstname=fname,
            lastname=lname,
            email_id=email,
            date_of_joining=doj,
            department=dept_object,
        )


        new_user.save()
        return HttpResponse("Successfully submitted")

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






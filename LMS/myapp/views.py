from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Employees, Department, Designation
from django.http import HttpResponse
from django.contrib.auth import get_user_model

# Create your views here.


def logins(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('dashboard')
            else:
                login(request, user)
                return redirect('emp_dashboard')

        # Handle invalid login here
        else:
            print("Invalid login attempt.")
            messages.error(request, "Invalid Credentials. Please check your username and password.")

    return render(request, 'login.html')

def forgotpass(request):
    return render(request, 'forgotpassword.html')

#employee
def empdashboard(request):
    return render(request, 'employee/dashboard.html')



#common
def applyleave(request):
    return render(request, 'applyleave.html')

def leavehistory(request):
    return render(request, 'leavehistory.html')

def profile(request):
    return render(request, 'profile.html')


#admin
def register(request):
    departments = Department.objects.values_list('dep_name', flat=True).distinct()
    if request.method == 'POST':
        empid = request.POST['empid']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        doj = request.POST['doj']
        desig = request.POST['desig']
        dept = request.POST['dept']
        password = request.POST['password']

        if dept == 'Other':
            other_dept = request.POST['other-dept']
            dept_object, created = Department.objects.get_or_create(dep_name=other_dept)
        else:
            dept_object, created = Department.objects.get_or_create(dep_name=dept)

        desig_object, created = Designation.objects.get_or_create(designation=desig, dep=dept_object)

        new_user = get_user_model().objects.create_user(
            email=email,
            password=password,
            emp_id=empid,
            firstname=fname,
            lastname=lname,
            date_of_joining=doj,
            department=dept_object,
        )

        return HttpResponse("Successfully submitted")

    return render(request, 'register.html', {'departments': departments})


def dashboard(request):
    return render(request, 'admin/dashboard.html')

def leaveRequest(request):
    return render(request,'admin/leaveRequest.html')

def emppage(request):
    return render(request, 'emppage.html')






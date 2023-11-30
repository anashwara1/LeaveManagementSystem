from decouple import config
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template.loader import get_template

from .models import Department, Designation
from django.contrib.auth.models import User
from .models import Employees, Department, Designation, Leavebalance, LeaveTypes, LeaveRequest, Managers
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import random


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
    if request.method == 'POST':
        email = request.POST['email']

        otp = random.randint(1000, 9999)

        subject = 'Changing Password'
        message = f'Change your password using this otp : {otp}'
        from_email = config('EMAIL_HOST_USER')
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        request.session['reset_otp'] = otp
        request.session['reset_email'] = email

        messages.success(request, 'Mail is sent. Please check your mail for the otp')
        return redirect('changepassword')

    return render(request, 'forgotpassword.html')


# employee
def empdashboard(request):
    return render(request, 'employee/dashboard.html')


# common
def applyleave(request):
    return render(request, 'applyleave.html')


def leavehistory(request):
    return render(request, 'leavehistory.html')


def profile(request):
    return render(request, 'profile.html')


# admin
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

        subject = 'Registration Confirmation'
        message = f'Your account have been successfully registered, {fname} {lname}!'
        from_email = config('EMAIL_HOST_USER')
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Employee registered successfully and mail is sent.')

    return render(request, 'register.html', {'departments': departments})


def dashboard(request):
    return render(request, 'admin/dashboard.html')


def leaveRequest(request):
    return render(request, 'admin/leaveRequest.html')


def emppage(request):
    return render(request, 'emppage.html')


def changepassword(request):
    if request.method == 'POST':
        newpass = request.POST['newpassword']
        confirmpass = request.POST['confirmpassword']
        otp = request.POST['otp']
        sentotp = request.session.get('reset_otp')

        if int(sentotp)!= int(otp):
            messages.error(request, f'OTP incorrect. Enter the correct otp{sentotp}')
        else:
            if newpass != confirmpass:
                messages.error(request, 'Password entered must be the same')
            else:
                email = request.session.get('reset_email')
                employee = Employees.objects.get(email=email)
                employee.password = make_password(newpass)
                employee.save()
                del request.session['reset_otp']
                del request.session['reset_email']
                messages.success(request, 'Password reset successful')
                return redirect('login')

    return render(request, 'changepassword.html')


# retrieving data from database to profile

@login_required
def profile(request):
    try:
        employee = Employees.objects.get(email=request.user.email)

        emp_id = employee.emp_id
        firstname = employee.firstname
        lastname = employee.lastname
        department = employee.department
        try:
            designation = Designation.objects.get(dep=department)
        except Designation.DoesNotExist:
            designation = None
        # Name = firstname + " " + lastname
        # department = employee.department
        # designation = department.dep.designation.designation if department and department.dep else None
        # department_name = department.Dep_Name
        # dateOfJoining = employee.date_of_joining
        # Manager = employee.managed_by
        try:
            leave_balance = Leavebalance.objects.get(empid=employee)
        except Leavebalance.DoesNotExist:
            # Handle the case where leave balance is not found
            leave_balance = None
        return render(request, 'profile.html', {
            'employee': employee,
            'emp_id': emp_id,
            'firstname': firstname,
            'lastname': lastname,

            'designation': designation,
            'department': department,
            'leave_balance': leave_balance,
            # 'dateOfJoining' : dateOfJoining,
            # 'Manager' :Manager,
        })
    except Employees.DoesNotExist:
        # Handle the case where the employee is not found
        return render(request, 'profile.html', {'error': 'Employee not found'})

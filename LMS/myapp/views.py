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

def manager_dashboard(request):

    manager = request.user

    # Get all employees managed by the manager
    employees_managed = Employees.objects.filter(managed_by=manager)

    context = {
        'employees_managed': employees_managed
    }

    return render(request, 'emppage.html', context)


def logins(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        request.session['logged_user'] = email
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


User = get_user_model()

def forgotpass(request):
    if request.method == 'POST':
        email = request.POST['email']


        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:

            messages.error(request, 'This email is not registered. Please enter a registered email address.')
            return redirect('forgotpassword')

        # User is found, proceed with the rest of your logic
        otp = random.randint(1000, 9999)

        subject = 'Changing Password'
        message = f'Change your password using this OTP: {otp}'
        from_email = config('EMAIL_HOST_USER')
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        request.session['reset_otp'] = otp
        request.session['reset_email'] = email

        messages.success(request, 'Mail is sent. Please check your mail for the OTP')
        return redirect('changepassword')

    return render(request, 'forgotpassword.html')

# employee
def empdashboard(request):
    return render(request, 'employee/dashboard.html')


# common
def applyleave(request):
    if request.method == 'POST':
        leavetype = request.POST['leavetype']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        reason = request.POST['reason']

        leaveTypeid_object, created = LeaveTypes.objects.get_or_create(leave_type_name=leavetype)
        emp_mail = request.session.get('logged_user')
        emp = Employees.objects.get(email=emp_mail)
        new_leave = LeaveRequest(
            startdate=startdate,
            enddate=enddate,
            reason=reason,
            leavetypeid=leaveTypeid_object,
            status='Pending',
            emp=emp
        )

        new_leave.save()
        messages.success(request, 'Leave Request sent successfully.')
    return render(request, 'applyleave.html')


def leavehistory(request):
    mail = request.session.get('logged_user')
    user = Employees.objects.get(email=mail)
    emp_leaves = LeaveRequest.objects.filter(emp=user.emp_id)
    context = {
        'leave_requests': emp_leaves,
    }
    return render(request, 'leavehistory.html', context)

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

        # Process the file upload
        employee_image = request.FILES.get('employee_image', None)

        # Save the uploaded image
        if employee_image:
            file_name = f"{empid}_{employee_image.name}"
            with open(f"media/profile_images/{file_name}", 'wb') as destination:
                for chunk in employee_image.chunks():
                    destination.write(chunk)
        else:
            file_name = None

        if dept == 'Other':
            other_dept = request.POST['other-dept']
            dept_object, created = Department.objects.get_or_create(dep_name=other_dept)
        else:
            dept_object, created = Department.objects.get_or_create(dep_name=dept)

        desig_object, created = Designation.objects.get_or_create(designation=desig, dep=dept_object)

        new_user = get_user_model().objects.create_user(
            emp_id=empid,
            firstname=fname,
            lastname=lname,
            email=email,
            password=password,
            date_of_joining=doj,
            department=dept_object,
            profile_image=f"profile_images/{file_name}" if file_name else None
        )

        subject = 'Registration Confirmation'
        message = f'Your account has been successfully registered, {fname} {lname}!'
        from_email = config('EMAIL_HOST_USER')
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Employee registered successfully, and an email is sent.')

       # return redirect('login')  # Redirect to login page after successful registration

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

        if int(sentotp) != int(otp):
            messages.error(request, 'OTP incorrect. Enter the correct otp')
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
        profile_image = employee.profile_image

        try:
             leave_balance = Leavebalance.objects.get(empid=employee)
        except Leavebalance.DoesNotExist:
                leave_balance = None

        return render(request, 'profile.html', {
                'employee': employee,
                'emp_id': emp_id,
                'firstname': firstname,
                'lastname': lastname,
                'profile_image': profile_image,
                'department': department,
                'leave_balance': leave_balance,
            })

    except Employees.DoesNotExist:
            return render(request, 'profile.html', {'error': 'Employee not found'})

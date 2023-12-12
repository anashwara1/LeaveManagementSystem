from decouple import config
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse


from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView

from .models import Department, Designation
from django.contrib.auth.models import User
from .models import Employees, Department, Designation, Leavebalance, LeaveTypes, LeaveRequest, Managers
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import random



class EditLeaveView(View):
    def post(self, request, leave_id, *args, **kwargs):
        leave = get_object_or_404(LeaveRequest, leave_request_id=leave_id)

        # Update leave details based on the POST data
        leave.leavetypeid_id = request.POST.get('leavetype')
        leave.startdate = request.POST.get('startdate')
        leave.enddate = request.POST.get('enddate')
        leave.reason = request.POST.get('reason')

        leave.save()

        return redirect('leavehistory')

class DeleteLeaveView(View):
    def post(self, request, leave_id, *args, **kwargs):
        leave = get_object_or_404(LeaveRequest, leave_request_id=leave_id)
        leave.delete()

        return redirect('leavehistory')


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_manager:
                login(request, user)
                return redirect('dashboard')
            else:
                login(request, user)
                return redirect('emp_dashboard')
        else:
            print("Invalid login attempt.")
            messages.error(request, "Invalid Credentials. Please check your username and password.")
            return render(request, self.template_name)


User = get_user_model()


class ForgotPassword(View):

    template_name = 'forgotpassword.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:

            messages.error(request, 'This email is not registered. Please enter a registered email address.')
            return redirect('forgotpassword')

        otp = random.randint(1000, 9999)
        fname = user.firstname
        lname = user.lastname
        subject = 'Forgot Password OTP'
        otp_template = config('FORGOT_PASSWORD_OTP_TEMPLATE')

        otp_template = otp_template.replace('\\n', '\n')
        message = otp_template.format(otp=otp,fname = fname,lname=lname)
        # message = f'Change your password using this otp : {otp}'
        from_email = config('EMAIL_HOST_USER')
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        request.session['reset_otp'] = otp
        request.session['reset_email'] = email

        messages.success(request, 'Mail is sent. Please check your mail for the OTP')
        return redirect('changepassword')



@method_decorator(login_required(login_url='/login'), name='dispatch')
class EmpDashboardView(TemplateView):
    template_name = 'employee/dashboard.html'

class LandingPageView(TemplateView):
    template_name = 'landingPage.html'


# common
@method_decorator(login_required(login_url='/login'), name='dispatch')
class ApplyLeave(View):
    template_name = 'applyleave.html'

    def post(self, request):
        leavetype = request.POST['leavetype']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        reason = request.POST['reason']

        leaveTypeid_object, created = LeaveTypes.objects.get_or_create(leave_type_name=leavetype)
        emp = Employees.objects.get(email=request.user.email)
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
        return render(request, self.template_name)

    def get(self, request,):
        return render(request, self.template_name)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaveHistory(View):
    template_name = 'leavehistory.html'

    def get(self, request):
        user = Employees.objects.get(email=request.user.email)
        emp_leaves = LeaveRequest.objects.filter(emp=user.emp_id)
        context = {
            'leave_requests': emp_leaves,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ResetPassword(View):
    template_name = 'resetpassword.html'

    def post(self, request):
        oldpass = request.POST['oldpassword']
        newpass = request.POST['newpassword']
        confirmpass = request.POST['confirmpassword']

        user = get_user_model().objects.get(email=request.user.email)

        if not check_password(oldpass, user.password):
            messages.error(request, 'The old password entered is wrong')
        else:
            if newpass != confirmpass:
                messages.error(request, 'Passwords entered must be the same')
            else:
                user.password = make_password(newpass)
                user.save()
                authenticated_user = authenticate(request, email=request.user.email, password=newpass)
                login(request, authenticated_user)
                messages.success(request, 'Password reset successful')
                return render(request, self.template_name)
        return render(request, self.template_name, {'messages': messages.get_messages(request)})

    def get(self, request):
        return render(request, self.template_name, {'messages': messages.get_messages(request)})




@login_required(login_url='/login')
def profile(request):
    return render(request, 'profile.html')


# admin
@method_decorator(login_required(login_url='/login'), name='dispatch')
class RegisterView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        departments = Department.objects.values_list('dep_name', flat=True).distinct()
        managers_id = Managers.objects.values_list('emp', flat=True).distinct()
        managers = Employees.objects.filter(emp_id__in=managers_id).values_list('firstname', flat=True)
        user = Employees.objects.get(email=request.user.email)
        context = {
            'departments': departments,
            'managers': managers
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        departments = Department.objects.values_list('dep_name', flat=True).distinct()
        managers_id = Managers.objects.values_list('emp', flat=True).distinct()
        managers = Employees.objects.filter(emp_id__in=managers_id).values_list('firstname', flat=True)
        user = Employees.objects.get(email=request.user.email)
        context = {
            'departments': departments,
            'managers': managers
        }

        empid = request.POST['empid']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        doj = request.POST['doj']
        desig = request.POST['desig']
        dept = request.POST['dept']
        password = request.POST['password']
        ismanager = request.POST['ismanager']
        manager = request.POST['manager']

        if len(empid) >= 10:
            messages.error(request, 'Entered employee ID is too long')
        else:
            # Process the file upload
            employee_image = request.FILES.get('employee_image', None)

            existing_employees = Employees.objects.filter(email=email)

            if existing_employees.exists():
                messages.error(request, 'Entered email is already registered')
            else:
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

                new_user = Employees.objects.create_user(
                    emp_id=empid,
                    firstname=fname,
                    lastname=lname,
                    email=email,
                    password=password,
                    date_of_joining=doj,
                    designation=desig_object,
                    balance=config('leave_initial'),
                    department=dept_object,
                    profile_image=f"profile_images/{file_name}" if file_name else None
                )

                if ismanager == 'yes':
                    newmanager, created = Managers.objects.get_or_create(emp=new_user)
                    new_user.is_manager = 'True'

                managerid = Employees.objects.get(firstname=manager)

                new_user.managed_by = Managers.objects.get(emp=managerid.emp_id)
                new_user.save()

                subject = 'Registration Confirmation'
                message_template = config('MESSAGE_TEMPLATE')

                message_template = message_template.replace('\\n','\n')
                message = message_template.format(fname=fname,lname=lname,email=email,password =password)

                from_email = config('EMAIL_HOST_USER')
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list)

                messages.success(request, 'Employee registered successfully')

        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='/login'), name='dispatch')
class Dashboard(View):
    template_name = 'admin/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaveRequestView(View):
    template_name = 'admin/leaveRequest.html'

    def get(self, request, *args, **kwargs):
        user = Employees.objects.get(email=request.user.email)
        manager = Managers.objects.get(emp=user.emp_id)
        emp_under_manager = Employees.objects.filter(managed_by=manager.manager_id)
        leaves = LeaveRequest.objects.filter(emp__in=emp_under_manager)
        for leave in leaves:
            leave.duration = (leave.enddate - leave.startdate).days + 1
        context = {
            'leaves': leaves
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = Employees.objects.get(email=request.user.email)
        manager = Managers.objects.get(emp=user.emp_id)
        emp_under_manager = Employees.objects.filter(managed_by=manager.manager_id)
        leaves = LeaveRequest.objects.filter(emp__in=emp_under_manager)
        for leave in leaves:
            leave.duration = (leave.enddate - leave.startdate).days + 1
        context = {
            'leaves': leaves
        }

        action = request.POST.get('action')
        leaveid = request.POST.get('empid')
        updated_leave = LeaveRequest.objects.get(leave_request_id=leaveid)

        if action == 'accept':
            updated_leave.status = 'Accepted'
        else:
            updated_leave.status = 'Rejected'

        updated_leave.save()

        email = Employees.objects.get(email=updated_leave.emp.email)
        subject = f'LEAVE REQUEST {action.upper()}ED'
        message = f'The leave request you have sent has been {action}ed'
        from_email = config('EMAIL_HOST_USER')
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        return redirect('leaveRequest')

@method_decorator(login_required(login_url='/login'), name='dispatch')
class EmployeePageView(View):
    template_name = 'emppage.html'
    error_template_name = 'error_page.html'

    def get(self, request, *args, **kwargs):
        manager_emp_id = request.user.emp_id

        try:
            manager_instance = Managers.objects.get(emp=manager_emp_id)
            manager_id = manager_instance.manager_id
        except Managers.DoesNotExist:
            return render(request, self.error_template_name)

        employees_managed = Employees.objects.filter(managed_by=manager_id)

        context = {
            'employees_managed': employees_managed,
            'manager_id': manager_id,
        }

        return render(request, self.template_name, context)

class ChangePassword(View):
    template_name = 'changepassword.html'

    def post(self, request):
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
        return render(request, self.template_name)

    def get(self, request):
        return render(request, self.template_name)


# retrieving data from database to profile


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
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

            context = {
                'employee': employee,
                'emp_id': emp_id,
                'firstname': firstname,
                'lastname': lastname,
                'profile_image': profile_image,
                'department': department,
                'leave_balance': leave_balance,
            }

            return render(request, self.template_name, context)

        except Employees.DoesNotExist:
            return render(request, self.template_name, {'error': 'Employee not found'})

class Logout(View):
    template_name = 'landingPage.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name)

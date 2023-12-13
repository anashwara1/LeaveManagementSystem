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

from .service import *

class EditLeaveView(View):
    def post(self, request, leave_id, *args, **kwargs):
        leavetype = request.POST.get('leavetype')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        reason = request.POST.get('reason')

        leave_service = LeaveService()
        leave_service.edit_leave(leave_id, leavetype, startdate, enddate, reason)
        return redirect('leavehistory')

class DeleteLeaveView(View):
    def post(self, request, leave_id, *args, **kwargs):
        leave_service = LeaveService()
        leave_service.delete_leave(leave_id)
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
    register_service = RegisterService()

    def get(self, request, *args, **kwargs):
        context = self.register_service.get_departments_and_managers()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
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

        context = self.register_service.register_employee(
            request, empid, fname, lname, email, doj, desig, dept, password, ismanager, manager
        )

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
        leave_request_service = LeaveRequestService()
        leaves = leave_request_service.get_leave_requests(user)
        context = {
            'leaves': leaves
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = Employees.objects.get(email=request.user.email)
        leave_request_service = LeaveRequestService()
        leaves = leave_request_service.get_leave_requests(user)

        action = request.POST.get('action')
        leave_id = request.POST.get('empid')

        leave_request_service.update_leave_status(leave_id, action)

        return redirect('leaveRequest')

@method_decorator(login_required(login_url='/login'), name='dispatch')
class EmployeePageView(View):
    template_name = 'emppage.html'
    error_template_name = 'error_page.html'

    def get(self, request, *args, **kwargs):
        manager_emp_id = request.user.emp_id

        employee_page_service = EmployeePageService()
        context = employee_page_service.get_managed_employees(manager_emp_id)

        if context is None:
            return render(request, self.error_template_name)

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
        email = request.user.email
        profile_service = ProfileService()
        context = profile_service.get_employee_profile(email)
        return render(request, self.template_name, context)


class Logout(View):
    template_name = 'landingPage.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name)

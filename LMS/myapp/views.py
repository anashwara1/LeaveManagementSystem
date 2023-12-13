from decouple import config
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from .services.service import *
from django.http import JsonResponse, HttpResponseRedirect
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
        loginservice = LoginService()
        redirect_url = loginservice.user_authentication(request, email, password)

        if redirect_url:
            return redirect(redirect_url)
        else:
            return render(request, self.template_name)


User = get_user_model()


class ForgotPassword(View):

    template_name = 'forgotpassword.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST['email']
        forgotpasswordservice = ForgotPasswordService()
        redirect_url = forgotpasswordservice.forgot_password_service(request, email)
        if redirect_url:
            return redirect(redirect_url)
        else:
            return render(request, self.template_name)

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

        applyleaveservice = ApplyLeaveService()
        applyleaveservice.apply_leave_service(request, startdate, enddate, reason, leavetype)
        return render(request, self.template_name)

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaveHistory(View):
    template_name = 'leavehistory.html'

    def get(self, request):
        leavehistoryservice = LeaveHistoryService()
        context = leavehistoryservice.leave_history_service(request)
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ResetPassword(View):
    template_name = 'resetpassword.html'

    def post(self, request):
        oldpass = request.POST['oldpassword']
        newpass = request.POST['newpassword']
        confirmpass = request.POST['confirmpassword']

        resetpasswordservice = ResetPasswordService()
        success, message = resetpasswordservice.reset_password_service(request, oldpass, newpass, confirmpass)

        if success:
            messages.success(request, message)
            return render(request, self.template_name)
        else:
            messages.error(request, message)
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

        changepasswordservice = ChangePasswordService()
        success, message = changepasswordservice.change_password_service(request, sentotp, otp, newpass, confirmpass)
        if success:
            messages.success(request, message)
            return redirect('login')
        else:
            messages.error(request, message)
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

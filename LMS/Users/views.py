from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from Users.services.service import UserService

# Create your views here.


userservice = UserService()

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST['username']
        password = request.POST['password']
        redirect_url = userservice.user_authentication(request, email, password)

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
        redirect_url = userservice.forgot_password_service(request, email)
        if redirect_url:
            return redirect(redirect_url)
        else:
            return render(request, self.template_name)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class EmpDashboardView(TemplateView):
    template_name = 'empdashboard.html'


class LandingPageView(TemplateView):
    template_name = 'landingPage.html'


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ResetPassword(View):
    template_name = 'resetpassword.html'

    def post(self, request):
        oldpass = request.POST['oldpassword']
        newpass = request.POST['newpassword']
        confirmpass = request.POST['confirmpassword']

        success, message = userservice.reset_password_service(request, oldpass, newpass, confirmpass)

        if success:
            messages.success(request, message)
            return render(request, self.template_name)
        else:
            messages.error(request, message)
            return render(request, self.template_name, {'messages': messages.get_messages(request)})

    def get(self, request):
        return render(request, self.template_name, {'messages': messages.get_messages(request)})


@method_decorator(login_required(login_url='/login'), name='dispatch')
class RegisterView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        context = userservice.get_departments_and_managers()
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

        context = userservice.register_employee(
            request, empid, fname, lname, email, doj, desig, dept, password, ismanager, manager
        )

        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class Dashboard(View):
    template_name = 'admindashboard.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class EmployeePageView(View):
    template_name = 'emppage.html'
    error_template_name = 'error_page.html'

    def get(self, request, *args, **kwargs):
        manager_emp_id = request.user.emp_id

        context = userservice.get_managed_employees(manager_emp_id)

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

        success, message = userservice.change_password_service(request, sentotp, otp, newpass, confirmpass)
        if success:
            messages.success(request, message)
            return redirect('login')
        else:
            messages.error(request, message)
            return render(request, self.template_name)

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        email = request.user.email
        context = userservice.get_employee_profile(email)
        return render(request, self.template_name, context)


class Logout(View):
    template_name = 'landingPage.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name)

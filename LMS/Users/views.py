from django.contrib import messages
from django.contrib.auth import get_user_model, logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from Users.models import Employees
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
        user = authenticate(request, email=email, password=password)

        if user is not None:
            redirect_url = userservice.user_authentication(user)
            login(request, user)
            return redirect(redirect_url)

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
        otp, redirect_url = userservice.forgot_password_service(email)

        request.session['reset_otp'] = otp
        request.session['reset_email'] = email

        if redirect_url == 'forgotpassword':
            messages.error(request, 'This email is not registered. Please enter a registered email address.')
            return redirect(redirect_url)

        elif redirect_url == 'changepassword':
            messages.success(request, 'Mail is sent. Please check your mail for the OTP')
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

        user = get_user_model().objects.get(email=request.user.email)

        success, message = userservice.reset_password_service(oldpass, newpass, confirmpass, user)

        if success:
            authenticated_user = authenticate(request, email=request.user.email, password=newpass)
            login(request, authenticated_user)
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

    def get(self, request):
        context = userservice.get_departments_and_managers()
        return render(request, self.template_name, context)

    def post(self, request):
        empid = request.POST['empid']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        doj = request.POST['doj']
        desig = request.POST['desig']
        dept = request.POST['dept']
        password = request.POST['password']
        ismanager = request.POST['ismanager']

        if dept == 'Other':
            other_dept = request.POST['other-dept']

        else:
            other_dept = None

        employee_image = request.FILES.get('employee_image', None)
        existing_employees = Employees.objects.filter(email=email)
        print(existing_employees.exists())

        if len(empid) >= 10:
            messages.error(request, 'Entered employee ID is too long')

        elif existing_employees.exists():
            messages.error(request, 'Entered email is already registered')

        else:
            messages.success(request, 'Employee registered successfully')

        context = userservice.register_employee(
            empid, fname, lname, email, doj, desig, dept, password, ismanager, employee_image, existing_employees, other_dept
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

    def get(self, request):
        service_data = userservice.get_managed_employees()
        employees_managed = service_data['employees_managed']

        departments_and_designations = userservice.get_departments_and_managers()
        departments = departments_and_designations['departments']
        designations = departments_and_designations['designations']

        context = {
            'employees_managed': employees_managed,
            'departments': departments,
            'designations': designations,
        }

        if context is None:
            return render(request, self.template_name)

        return render(request, self.template_name, context)

    def post(self, request):

        form_type = request.POST['form_type']
        if form_type == 'form1':
            empid = request.POST['empid']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            dep = request.POST['dept']
            desig = request.POST['desig']
            doj = request.POST['doj']
            manager = request.POST['ismanager']
            redirect_url = userservice.update_user(empid, fname, lname, email, dep, desig, doj, manager)

        else:
            employee_id = request.POST['emp-id']
            startdate = request.POST['startdate']
            enddate = request.POST['enddate']
            lopdays = request.POST['noofdays']
            remarks = request.POST['remarks']
            redirect_url = userservice.lop(startdate, enddate, lopdays, employee_id, remarks)

        messages.success(request, 'Employee details updated successfully')

        return redirect(redirect_url)


class ChangePassword(View):
    template_name = 'changepassword.html'

    def post(self, request):
        newpass = request.POST['newpassword']
        confirmpass = request.POST['confirmpassword']
        otp = request.POST['otp']
        sentotp = request.session.get('reset_otp')
        email = request.session.get('reset_email')

        success, message = userservice.change_password_service(sentotp, otp, newpass, confirmpass, email)
        if success:
            del request.session['reset_otp']
            del request.session['reset_email']
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

    def get(self, request):
        email = request.user.email
        context = userservice.get_employee_profile(email)
        return render(request, self.template_name, context)


class Logout(View):
    template_name = 'landingPage.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name)


class DeleteEmployee(View):
    def post(self, request, emp_id, *args, **kwargs):
        redirect_url = userservice.delete_employee(emp_id)
        return redirect(redirect_url)


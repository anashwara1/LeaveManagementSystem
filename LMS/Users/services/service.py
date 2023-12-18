import random
from decouple import config
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from Users.models import *


class UserService:
    def user_authentication(self, request, email, password):
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return 'dashboard'
            else:
                login(request, user)
                return 'emp_dashboard'
        else:
            print("Invalid login attempt.")
            messages.error(request, "Invalid Credentials. Please check your username and password.")
            return None

    def forgot_password_service(self, request, email):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:

            messages.error(request, 'This email is not registered. Please enter a registered email address.')
            return 'forgotpassword'

        otp = random.randint(1000, 9999)
        fname = user.first_name
        lname = user.last_name
        subject = 'Forgot Password OTP'
        otp_template = config('FORGOT_PASSWORD_OTP_TEMPLATE')

        otp_template = otp_template.replace('\\n', '\n')
        message = otp_template.format(otp=otp, fname=fname, lname=lname)
        from_email = config('EMAIL_HOST_USER')
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        request.session['reset_otp'] = otp
        request.session['reset_email'] = email

        messages.success(request, 'Mail is sent. Please check your mail for the OTP')
        return 'changepassword'

    def reset_password_service(self, request, oldpass, newpass, confirmpass):
        user = get_user_model().objects.get(email=request.user.email)

        if not check_password(oldpass, user.password):
            return False, 'The old password entered is wrong'
        else:
            if newpass != confirmpass:
                return False, 'Passwords entered must be the same'
            else:
                user.password = make_password(newpass)
                user.save()
                authenticated_user = authenticate(request, email=request.user.email, password=newpass)
                login(request, authenticated_user)
                return True, 'Password reset successful'

    def change_password_service(self, request, sentotp, otp, newpass, confirmpass):
        if int(sentotp) != int(otp):
            return False, 'OTP incorrect. Enter the correct otp'
        else:
            if newpass != confirmpass:
                return False, 'Password entered must be the same'
            else:
                email = request.session.get('reset_email')
                employee = Employees.objects.get(email=email)
                employee.password = make_password(newpass)
                employee.save()
                del request.session['reset_otp']
                del request.session['reset_email']
                return True, 'Password reset successful'

    def get_employee_profile(self, email):
        try:
            employee = Employees.objects.get(email=email)
            return {
                'employee': employee
            }

        except Employees.DoesNotExist:
            return {'error': 'Employee not found'}

    def get_managed_employees(self, manager_emp_id):
        try:
            manager_instance = Employees.objects.filter(is_staff=False)
        except Employees.DoesNotExist:
            return None

        return {
            'employees_managed': manager_instance,
        }

    def get_departments_and_managers(self):
        departments = Department.objects.values_list('dep_name', flat=True).distinct()
        designations = Designation.objects.values_list('designation', flat=True).distinct()

        return {
            'departments': departments,
            'designations': designations,
        }

    def register_employee(self, request, empid, fname, lname, email, doj, desig, dept, password, ismanager):
        context = self.get_departments_and_managers()

        if len(empid) >= 10:
            messages.error(request, 'Entered employee ID is too long')
            return context

        employee_image = request.FILES.get('employee_image', None)
        existing_employees = Employees.objects.filter(email=email)

        if existing_employees.exists():
            messages.error(request, 'Entered email is already registered')
            return context

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
            first_name=fname,
            last_name=lname,
            email=email,
            password=password,
            date_of_joining=doj,
            designation=desig_object,
            profile_image=f"profile_images/{file_name}" if file_name else None
        )

        if ismanager == 'yes':
            new_user.is_staff = 'True'

        subject = 'Registration Confirmation'
        message_template = config('MESSAGE_TEMPLATE')

        message_template = message_template.replace('\\n', '\n')
        message = message_template.format(fname=fname, lname=lname, email=email, password=password)

        from_email = config('EMAIL_HOST_USER')
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Employee registered successfully')

        return context

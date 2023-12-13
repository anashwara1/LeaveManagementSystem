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
            if user.is_manager:
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
        fname = user.firstname
        lname = user.lastname
        subject = 'Forgot Password OTP'
        otp_template = config('FORGOT_PASSWORD_OTP_TEMPLATE')

        otp_template = otp_template.replace('\\n', '\n')
        message = otp_template.format(otp=otp, fname=fname,lname=lname)
        # message = f'Change your password using this otp : {otp}'
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
            emp_id = employee.emp_id
            firstname = employee.firstname
            lastname = employee.lastname
            department = employee.department
            profile_image = employee.profile_image


            return {
                'employee': employee,
                'emp_id': emp_id,
                'firstname': firstname,
                'lastname': lastname,
                'profile_image': profile_image,
                'department': department,
            }

        except Employees.DoesNotExist:
            return {'error': 'Employee not found'}

    def get_managed_employees(self, manager_emp_id):
        try:
            manager_instance = Managers.objects.get(emp=manager_emp_id)
            manager_id = manager_instance.manager_id
        except Managers.DoesNotExist:
            return None

        employees_managed = Employees.objects.filter(managed_by=manager_id)
        return {
            'employees_managed': employees_managed,
            'manager_id': manager_id,
        }

    def get_departments_and_managers(self):
        departments = Department.objects.values_list('dep_name', flat=True).distinct()
        managers_id = Managers.objects.values_list('emp', flat=True).distinct()
        managers = Employees.objects.filter(emp_id__in=managers_id).values_list('firstname', flat=True)

        return {
            'departments': departments,
            'managers': managers
        }

    def register_employee(self, request, empid, fname, lname, email, doj, desig, dept, password, ismanager, manager):
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

        message_template = message_template.replace('\\n', '\n')
        message = message_template.format(fname=fname, lname=lname, email=email, password=password)

        from_email = config('EMAIL_HOST_USER')
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Employee registered successfully')

        return context

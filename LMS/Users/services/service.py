import random
from decouple import config
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from Users.models import *


class UserService:
    def user_authentication(self, user):

        if user.is_staff:
            return 'dashboard'
        else:
            return 'emp_dashboard'


    def forgot_password_service(self, email):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None, 'forgotpassword'

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

        return otp, 'changepassword'

    def reset_password_service(self, oldpass, newpass, confirmpass, user):

        if not check_password(oldpass, user.password):
            return False, 'The old password entered is wrong'
        else:
            if newpass != confirmpass:
                return False, 'Passwords entered must be the same'
            else:
                user.password = make_password(newpass)
                user.save()
                return True, 'Password reset successful'

    def change_password_service(self, sentotp, otp, newpass, confirmpass, email):
        if int(sentotp) != int(otp):
            return False, 'OTP incorrect. Enter the correct otp'
        else:
            if newpass != confirmpass:
                return False, 'Password entered must be the same'
            else:
                employee = Employees.objects.get(email=email)
                employee.password = make_password(newpass)
                employee.save()
                return True, 'Password reset successful'

    def get_employee_profile(self, email):
        try:
            employee = Employees.objects.get(email=email)
            return {
                'employee': employee
            }

        except Employees.DoesNotExist:
            return {'error': 'Employee not found'}

    def get_managed_employees(self):
        try:
            manager_instance = Employees.objects.filter(is_superuser=False, is_active=True)
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

    def register_employee(self, empid, fname, lname, email, doj, desig, dept, password, ismanager, employee_image, existing_employees, other_dept):
        context = self.get_departments_and_managers()

        if len(empid) >= 10:
            return context

        if existing_employees.exists():
            return context

        if employee_image:
            file_name = f"{empid}_{employee_image.name}"
            with open(f"media/profile_images/{file_name}", 'wb') as destination:
                for chunk in employee_image.chunks():
                    destination.write(chunk)
        else:
            file_name = None

        if dept == 'Other':
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
            new_user.save()

        subject = 'Registration Confirmation'
        message_template = config('MESSAGE_TEMPLATE')

        message_template = message_template.replace('\\n', '\n')
        message = message_template.format(fname=fname, lname=lname, email=email, password=password)

        from_email = config('EMAIL_HOST_USER')
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        return context

    def update_user(self, empid, fname, lname, email, dep, desig, doj, manager):
        user = Employees.objects.get(emp_id=empid)
        user.first_name = fname
        user.last_name = lname
        user.email = email
        dept_object, created = Department.objects.get_or_create(dep_name=dep)
        desig_object, created = Designation.objects.get_or_create(designation=desig, dep=dept_object)
        user.designation = desig_object
        user.date_of_joining = doj
        if manager == 'yes':
            user.is_staff = True

        elif manager == 'no':
            user.is_staff = False

        user.save()
        return 'employees'

    def delete_employee(self, employee_id):
        employee = get_object_or_404(Employees, emp_id=employee_id)
        employee.is_active = False
        employee.save()
        return 'employees'
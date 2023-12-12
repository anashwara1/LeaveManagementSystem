from decouple import config
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import *

class LeaveService:
    @staticmethod
    def edit_leave(leave_id, leavetype, startdate, enddate, reason):
        leave = get_object_or_404(LeaveRequest, leave_request_id=leave_id)

        # Update leave details based on the provided data
        leave.leavetypeid_id = leavetype
        leave.startdate = startdate
        leave.enddate = enddate
        leave.reason = reason

        leave.save()

    @staticmethod
    def delete_leave(leave_id):
        leave = get_object_or_404(LeaveRequest, leave_request_id=leave_id)
        leave.delete()



class ProfileService:
    @staticmethod
    def get_employee_profile(email):
        try:
            employee = Employees.objects.get(email=email)
            emp_id = employee.emp_id
            firstname = employee.firstname
            lastname = employee.lastname
            department = employee.department
            profile_image = employee.profile_image

            try:
                leave_balance = Leavebalance.objects.get(empid=employee)
            except Leavebalance.DoesNotExist:
                leave_balance = None

            return {
                'employee': employee,
                'emp_id': emp_id,
                'firstname': firstname,
                'lastname': lastname,
                'profile_image': profile_image,
                'department': department,
                'leave_balance': leave_balance,
            }

        except Employees.DoesNotExist:
            return {'error': 'Employee not found'}


class EmployeePageService:
    @staticmethod
    def get_managed_employees(manager_emp_id):
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


class LeaveRequestService:
    @staticmethod
    def get_leave_requests(user):
        manager = Managers.objects.get(emp=user.emp_id)
        emp_under_manager = Employees.objects.filter(managed_by=manager.manager_id)
        leaves = LeaveRequest.objects.filter(emp__in=emp_under_manager)
        for leave in leaves:
            leave.duration = (leave.enddate - leave.startdate).days + 1
        return leaves

    @staticmethod
    def update_leave_status(leave_id, action):
        updated_leave = LeaveRequest.objects.get(leave_request_id=leave_id)

        if action == 'accept':
            updated_leave.status = 'Accepted'
        else:
            updated_leave.status = 'Rejected'

        updated_leave.save()

        email = Employees.objects.get(email=updated_leave.emp.email)
        subject = f'LEAVE REQUEST {action.upper()}ED'
        message = f'The leave request you have sent has been {action}ed'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email.email]

        send_mail(subject, message, from_email, recipient_list)


class RegisterService:
    @staticmethod
    def get_departments_and_managers():
        departments = Department.objects.values_list('dep_name', flat=True).distinct()
        managers_id = Managers.objects.values_list('emp', flat=True).distinct()
        managers = Employees.objects.filter(emp_id__in=managers_id).values_list('firstname', flat=True)

        return {
            'departments': departments,
            'managers': managers
        }

    @staticmethod
    def register_employee(request, empid, fname, lname, email, doj, desig, dept, password, ismanager, manager):
        context = RegisterService.get_departments_and_managers()

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
            balance=config('leave_initial'),  # Access LEAVE_INITIAL using config
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
        message_template = config('MESSAGE_TEMPLATE')  # Access MESSAGE_TEMPLATE using config

        message_template = message_template.replace('\\n', '\n')
        message = message_template.format(fname=fname, lname=lname, email=email, password=password)

        from_email = config('EMAIL_HOST_USER')  # Access EMAIL_HOST_USER using config
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Employee registered successfully')

        return context
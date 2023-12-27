from django.conf import settings
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import numpy as np
from Users.models import Employees
from leaves.models import *
import calendar


class ApplyLeaveService:

    def get_leave_types(self):
        leavetypes = LeaveTypes.objects.all().distinct()
        return leavetypes

    def apply_leave_service(self, startdate, enddate, reason, leavetype, emp):
        leaveTypeid_object, created = LeaveTypes.objects.get_or_create(leave_type_name=leavetype)
        try:
            leave_requests = LeaveRequest.objects.filter(startdate__range=(startdate, enddate), enddate__range=(startdate, enddate), emp=emp.emp_id)
            if leave_requests.exists():
                return True
            else:
                new_leave = LeaveRequest(
                    startdate=startdate,
                    enddate=enddate,
                    reason=reason,
                    leavetypeid=leaveTypeid_object,
                    emp=emp
                )

                if emp.is_superuser:
                    new_leave.status = 'Accepted'
                else:
                    new_leave.status = 'Pending'
                new_leave.save()
                return False

        except IntegrityError:
            return False


class LeaveHistoryService:
    def leave_history_service(self, user):
        emp_leaves = LeaveRequest.objects.filter(emp=user.emp_id)
        context = {
            'leave_requests': emp_leaves,
        }
        return context


class LeaveService:
    def get_leave(self, leave_id):
        return get_object_or_404(LeaveRequest, leave_request_id=leave_id)

    def edit_leave(self, leave_id, leavetype, startdate, enddate, reason):
        leave = self.get_leave(leave_id)
        leavetype = LeaveTypes.objects.get(leave_type_id=leavetype)
        leave.leavetypeid = leavetype
        leave.startdate = startdate
        leave.enddate = enddate
        leave.reason = reason
        leave.save()

    def delete_leave(self, leave_id):
        leave = self.get_leave(leave_id)
        leave.delete()


class LeaveRequestService:
    def get_leave_requests(self):
        try:
            emp_under_manager = Employees.objects.filter(is_staff=False)
            leaves = LeaveRequest.objects.filter(emp__in=emp_under_manager)
            try:
                holidays = Holidays.objects.all()
                holidays_array = []
                for holiday in holidays:
                    holidays_array.append(holiday.date)
                    print(holidays_array)

            except Holidays.DoesNotExist:
                holidays_array = []

            for leave in leaves:
                leave.duration = np.busday_count(leave.startdate, leave.enddate, weekmask='1111100', holidays=holidays_array) + 1

            return leaves

        except (Employees.DoesNotExist, LeaveRequest.DoesNotExist):
            return None

        except e:
            return None

    def update_leave_status(self, leave_id, action):
        try:
            updated_leave = LeaveRequest.objects.get(leave_request_id=leave_id)
        except LeaveRequest.DoesNotExist:
            print('Leave is not found')

        try:
            holidays = Holidays.objects.all()
            holidays_array = []
            for holiday in holidays:
                holidays_array.append(holiday.date)
                print(holidays_array)

        except Holidays.DoesNotExist:
            holidays_array = []

        duration = np.busday_count(updated_leave.startdate, updated_leave.enddate, weekmask='1111100', holidays=holidays_array) + 1
        leave_consumed, created = Leavebalance.objects.get_or_create(empid=updated_leave.emp)
        if leave_consumed.leave_consumed is None:
            leave_consumed.leave_consumed = 0
        if action == 'accept':
            updated_leave.status = 'Approved'
            leave_consumed.leave_consumed += duration
            leave_consumed.save()

        else:
            updated_leave.status = 'Rejected'

        updated_leave.save()

        email = Employees.objects.get(email=updated_leave.emp.email)
        subject = f'LEAVE REQUEST {action.upper()}ED'
        message = f'The leave request you have sent has been {action}ed'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email.email]

        send_mail(subject, message, from_email, recipient_list)


class HolidayService:

    def new_holiday(self, hname, hdate):
        try:
            holidays, created = Holidays.objects.get_or_create(date=hdate)
            holidays.holiday_name = hname
            holidays.date = hdate
            input_date = tuple(map(int, hdate.split('-')))
            day_name = calendar.weekday(*input_date)
            holidays.day = calendar.day_name[day_name]
            holidays.save()
            return 'holidays', 'Successfully added new holiday'

        except e:
            return 'holidays', 'Could not add new holiday'

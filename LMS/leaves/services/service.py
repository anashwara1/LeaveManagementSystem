from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from Users.models import Employees, Managers
from leaves.models import LeaveTypes, LeaveRequest


class ApplyLeaveService:

    def get_leave_types(self):
        leavetypes = LeaveTypes.objects.all().distinct()
        return leavetypes

    def apply_leave_service(self, request, startdate, enddate, reason, leavetype):
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


class LeaveHistoryService:
    def leave_history_service(self, request):
        user = Employees.objects.get(email=request.user.email)
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
    def get_leave_requests(self, user):
        manager = Managers.objects.get(emp=user.emp_id)
        emp_under_manager = Employees.objects.filter(managed_by=manager.manager_id)
        leaves = LeaveRequest.objects.filter(emp__in=emp_under_manager)
        for leave in leaves:
            leave.duration = (leave.enddate - leave.startdate).days + 1
        return leaves

    def update_leave_status(self, leave_id, action):
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

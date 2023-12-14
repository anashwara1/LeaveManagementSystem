from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from Users.models import Employees
from leaves.services.service import LeaveService, ApplyLeaveService, LeaveHistoryService, LeaveRequestService


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
        applyleaveservice = ApplyLeaveService()
        context = {
            'leavetypes': applyleaveservice.get_leave_types()}
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaveHistory(View):
    template_name = 'leavehistory.html'

    def get(self, request):
        leavehistoryservice = LeaveHistoryService()
        context = leavehistoryservice.leave_history_service(request)
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaveRequestView(View):
    template_name = 'leaveRequest.html'

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

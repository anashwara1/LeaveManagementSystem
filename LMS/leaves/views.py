from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from leaves.models import *
from Users.models import Employees
from leaves.services.service import *


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
        emp = Employees.objects.get(email=request.user.email)

        applyleaveservice = ApplyLeaveService()
        existing_leave_request = applyleaveservice.apply_leave_service(startdate, enddate, reason, leavetype, emp)
        if existing_leave_request:
            messages.error(request, 'Leave for this day is already applied')
            return redirect('leavehistory')
        else:
            messages.success(request, 'Leave Request sent successfully.')
            return redirect('leavehistory')

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
        user = Employees.objects.get(email=request.user.email)
        context = leavehistoryservice.leave_history_service(user)
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaveRequestView(View):
    template_name = 'leaveRequest.html'

    def get(self, request, *args, **kwargs):
        user = Employees.objects.get(email=request.user.email)
        leave_request_service = LeaveRequestService()
        leaves = leave_request_service.get_leave_requests()
        context = {
            'leaves': leaves
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = Employees.objects.get(email=request.user.email)
        leave_request_service = LeaveRequestService()
        leaves = leave_request_service.get_leave_requests()

        action = request.POST.get('action')
        leave_id = request.POST.get('empid')

        message = leave_request_service.update_leave_status(leave_id, action)

        return redirect('leaveRequest')


class Holiday(View):
    template_name = 'holidays.html'

    def get(self, request):
        try:
            holidays = Holidays.objects.all()
        except Holidays.DoesNotExist:
            holidays = None

        context = {
            'holidays': holidays
        }

        return render(request, self.template_name, context)

    def post(self, request):
        hname = request.POST['name']
        hdate = request.POST['date']
        holiday_service = HolidayService()
        redirect_url, message = holiday_service.new_holiday(hname, hdate)
        return redirect(redirect_url)

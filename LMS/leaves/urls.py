from django.urls import path
from .views import *

urlpatterns = [

    path('leaveRequest', LeaveRequestView.as_view(), name='leaveRequest'),
    path('applyleave/', ApplyLeave.as_view(), name='applyleave'),
    path('leavehistory/', LeaveHistory.as_view(), name='leavehistory'),
    path('edit_leave/<int:leave_id>/', EditLeaveView.as_view(), name='edit_leave'),
    path('delete_leave/<int:leave_id>/', DeleteLeaveView.as_view(), name='delete_leave'),
    path('holidays/', Holiday.as_view(), name='holidays'),
    path('error/', ErrorPageView.as_view(), name='errorpage'),

]

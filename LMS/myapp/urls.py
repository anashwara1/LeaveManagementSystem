from django.contrib import admin
from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('forgotpassword/', ForgotPassword.as_view(), name='forgotpassword'),
    path('', views.LandingPageView.as_view(), name='landingPage'),
    #employee
    path('emp_dashboard/', EmpDashboardView.as_view(), name='emp_dashboard'),
    #admin
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('leaveRequest', LeaveRequestView.as_view(), name='leaveRequest'),
    path('employees/', EmployeePageView.as_view(), name='employees'),
    path('register_user/', RegisterView.as_view(), name='register'),
    #common
    path('applyleave/', ApplyLeave.as_view(), name='applyleave'),
    path('leavehistory/', LeaveHistory.as_view(), name='leavehistory'),
    path('change_password/', ChangePassword.as_view(), name='changepassword'),
    path('reset_password/', ResetPassword.as_view(), name='resetpassword'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_leave/<int:leave_id>/',EditLeaveView.as_view(), name='edit_leave'),
    path('delete_leave/<int:leave_id>/', DeleteLeaveView.as_view(), name='delete_leave'),

]

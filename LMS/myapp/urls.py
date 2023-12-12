from django.contrib import admin
from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', views.landingPage, name='landingPage'),
    path('forgotpassword/', ForgotPassword.as_view(), name='forgotpassword'),
    #employee
    path('emp_dashboard/', views.empdashboard, name='emp_dashboard'),
    #admin
    path('leaveRequest', views.leaveRequest, name='leaveRequest'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('employees/', views.emppage, name='employees'),
    path('register_user/', views.register, name='register'),
    #common
    path('applyleave/', ApplyLeave.as_view(), name='applyleave'),
    path('leavehistory/', LeaveHistory.as_view(), name='leavehistory'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', ChangePassword.as_view(), name='changepassword'),
    path('reset_password/', ResetPassword.as_view(), name='resetpassword'),
    path('logout/', Logout.as_view(), name='logout'),
    path('get_leave/<int:leave_id>/', views.get_leave, name='get_leave'),
    path('edit_leave/<int:leave_id>/',views.edit_leave, name='edit_leave'),
    path('delete_leave/<int:leave_id>/', views.delete_leave, name='delete_leave'),

]

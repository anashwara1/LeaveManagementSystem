from django.contrib import admin
from django.urls import path
from . import views
from .views import EditLeaveView, DeleteLeaveView, EmpDashboardView, ProfileView, EmployeePageView, LeaveRequestView, \
    RegisterView

urlpatterns = [
    path('login/', views.logins, name='login'),
    path('', views.LandingPageView.as_view(), name='landingPage'),
    path('forgotpassword/', views.forgotpass, name='forgotpassword'),
    #employee
    path('emp_dashboard/', EmpDashboardView.as_view(), name='emp_dashboard'),
    #admin
    path('leaveRequest', LeaveRequestView.as_view(), name='leaveRequest'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees/', EmployeePageView.as_view(), name='employees'),
    path('register_user/', RegisterView.as_view(), name='register'),
    #common
    path('applyleave/', views.applyleave, name='applyleave'),
    path('leavehistory/', views.leavehistory, name='leavehistory'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change_password/', views.changepassword, name='changepassword'),
    path('reset_password/', views.resetpassword, name='resetpassword'),
    path('logout/', views.logout_view, name='logout'),
    # path('get_leave/<int:leave_id>/', views.get_leave, name='get_leave'),
    path('edit_leave/<int:leave_id>/',EditLeaveView.as_view(), name='edit_leave'),
    path('delete_leave/<int:leave_id>/', DeleteLeaveView.as_view(), name='delete_leave'),

]

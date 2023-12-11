from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.logins, name='login'),
    path('', views.landingPage, name='landingPage'),
    path('forgotpassword/', views.forgotpass, name='forgotpassword'),
    #employee
    path('emp_dashboard/', views.empdashboard, name='emp_dashboard'),
    #admin
    path('leaveRequest', views.leaveRequest, name='leaveRequest'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees/', views.emppage, name='employees'),
    path('register_user/', views.register, name='register'),
    #common
    path('applyleave/', views.applyleave, name='applyleave'),
    path('leavehistory/', views.leavehistory, name='leavehistory'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.changepassword, name='changepassword'),
    path('reset_password/', views.resetpassword, name='resetpassword'),
    path('logout/', views.logout_view, name='logout'),
    path('get_leave/<int:leave_id>/', views.get_leave, name='get_leave'),
    path('edit_leave/<int:leave_id>/',views.edit_leave, name='edit_leave'),
    path('delete_leave/<int:leave_id>/', views.delete_leave, name='delete_leave'),

]

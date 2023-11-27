from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.logins, name='login'),
    path('forgotpassword/', views.forgotpass, name='forgotpassword'),
    #employee
    path('emp_dashboard/', views.empdashboard, name='emp_dashboard'),
    #admin
    path('leaveRequest',views.leaveRequest,name='leaveRequest'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees/', views.emppage, name='employees'),
    path('register_user/', views.register, name='register'),
    #common
    path('applyleave/', views.applyleave, name='applyleave'),
    path('leavehistory/', views.leavehistory, name='leavehistory'),
    path('profile/', views.profile, name='profile'),

]

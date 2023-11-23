from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.logins, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgotpassword/', views.forgotpass, name='forgotpassword'),
    path('applyleave/', views.applyleave, name='applyleave'),
    path('leavehistory/', views.leavehistory, name='leavehistory'),
    path('profile/', views.profile, name='profile'),
    path('employees/', views.emppage, name='employee'),
    path('register_user/', views.register, name='register'),
    path('emp_dashboard/', views.empdashboard, name='emp_dashboard')
]

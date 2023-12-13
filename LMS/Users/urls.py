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
    path('employees/', EmployeePageView.as_view(), name='employees'),
    path('register_user/', RegisterView.as_view(), name='register'),
    #common
    path('change_password/', ChangePassword.as_view(), name='changepassword'),
    path('reset_password/', ResetPassword.as_view(), name='resetpassword'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

]

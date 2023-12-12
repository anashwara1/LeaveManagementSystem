from decouple import config
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
import random
from myapp.models import *


def user_authentication(request, email, password):
    user = authenticate(request, email=email, password=password)

    if user is not None:
        if user.is_manager:
            login(request, user)
            return 'dashboard'
        else:
            login(request, user)
            return 'emp_dashboard'
    else:
        print("Invalid login attempt.")
        messages.error(request, "Invalid Credentials. Please check your username and password.")
        return None


def forgot_password_service(request, email):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:

        messages.error(request, 'This email is not registered. Please enter a registered email address.')
        return 'forgotpassword'

    otp = random.randint(1000, 9999)
    fname = user.firstname
    lname = user.lastname
    subject = 'Forgot Password OTP'
    otp_template = config('FORGOT_PASSWORD_OTP_TEMPLATE')

    otp_template = otp_template.replace('\\n', '\n')
    message = otp_template.format(otp=otp, fname=fname,lname=lname)
    # message = f'Change your password using this otp : {otp}'
    from_email = config('EMAIL_HOST_USER')
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

    request.session['reset_otp'] = otp
    request.session['reset_email'] = email

    messages.success(request, 'Mail is sent. Please check your mail for the OTP')
    return 'changepassword'


def apply_leave_service(request, startdate, enddate, reason, leavetype):
    leaveTypeid_object, created = LeaveTypes.objects.get_or_create(leave_type_name=leavetype)
    emp = Employees.objects.get(email=request.user.email)
    new_leave = LeaveRequest(
        startdate=startdate,
        enddate=enddate,
        reason=reason,
        leavetypeid=leaveTypeid_object,
        status='Pending',
        emp=emp
    )

    new_leave.save()
    messages.success(request, 'Leave Request sent successfully.')


def leave_history_service(request):
    user = Employees.objects.get(email=request.user.email)
    emp_leaves = LeaveRequest.objects.filter(emp=user.emp_id)
    context = {
        'leave_requests': emp_leaves,
    }
    return context


def reset_password_service(request, oldpass, newpass, confirmpass):
    user = get_user_model().objects.get(email=request.user.email)

    if not check_password(oldpass, user.password):
        return False, 'The old password entered is wrong'
    else:
        if newpass != confirmpass:
            return False, 'Passwords entered must be the same'
        else:
            user.password = make_password(newpass)
            user.save()
            authenticated_user = authenticate(request, email=request.user.email, password=newpass)
            login(request, authenticated_user)
            return True, 'Password reset successful'

def change_password_service(request, sentotp, otp, newpass, confirmpass):
    if int(sentotp) != int(otp):
        return False, 'OTP incorrect. Enter the correct otp'
    else:
        if newpass != confirmpass:
            return False, 'Password entered must be the same'
        else:
            email = request.session.get('reset_email')
            employee = Employees.objects.get(email=email)
            employee.password = make_password(newpass)
            employee.save()
            del request.session['reset_otp']
            del request.session['reset_email']
            return True, 'Password reset successful'
